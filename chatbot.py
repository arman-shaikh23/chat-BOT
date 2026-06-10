import os, json, httpx, pathlib, argparse, sys, time, random
from config import MAX_RETRIES, BASE_BACKOFF_DELAY, AVG_CHARS_PER_TOKEN

# Terminal Colors
G, B, R, Y, C = '\033[92m', '\033[94m', '\033[0m', '\033[93m', '\033[96m'

def load_env():
    """Loads environment variables from .env file."""
    p = pathlib.Path('.env')
    if p.exists():
        for line in p.read_text(encoding='utf-8').splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

def get_config(provider):
    configs = {
        "nvidia": {
            "url": "https://integrate.api.nvidia.com/v1/chat/completions",
            "key_env": "NVIDIA_API_KEY",
            "model": "meta/llama-3.1-8b-instruct",
            "headers": lambda key: {"Authorization": f"Bearer {key}"}
        },
        "openrouter": {
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "key_env": "OPENROUTER_API_KEY",
            "model": "nex-agi/nex-n2-pro:free",
            "headers": lambda key: {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "CLI Chatbot"
            }
        },
        "gemini": {
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent",
            "key_env": "GEMINI_API_KEY",
            "headers": lambda key: {"Content-Type": "application/json"}
        }
    }
    return configs.get(provider)

def count_tokens(text):
    """Simple token estimation based on character count."""
    return len(text) // AVG_CHARS_PER_TOKEN

def handle_api_error(status_code, error_body=""):
    """Maps API status codes to user-friendly messages."""
    try:
        data = json.loads(error_body)
        error_msg = data.get('error', {}).get('message', '') or data.get('message', '')
    except:
        error_msg = error_body

    messages = {
        401: "Invalid API key. Please check your .env file.",
        403: "Access forbidden. You might not have permission for this model or resource.",
        404: "Model or resource not found. Please check the model name or API configuration.",
        429: "Rate limit reached. Retrying with exponential backoff...",
        500: "Server error (500). The provider is experiencing internal issues.",
        502: "Bad Gateway (502). The provider's server is likely down.",
        503: "Service Unavailable (503). The provider is overloaded or down for maintenance.",
        504: "Gateway Timeout (504). The provider's server took too long to respond."
    }
    
    friendly = messages.get(status_code, f"Unexpected error (Status {status_code})")
    print(f"\n{R}{friendly}{R}")
    if error_msg and status_code not in messages:
        print(f"{R}Details: {error_msg}{R}\n")
    else:
        print("")

def handle_exception(e):
    """Handles httpx and other network-related exceptions."""
    if isinstance(e, httpx.TimeoutException):
        print(f"\n{R}Request timed out. Retrying...{R}\n")
    elif isinstance(e, httpx.ConnectError):
        print(f"\n{R}Network error: Could not connect to the server. Please check your internet connection.{R}\n")
    elif isinstance(e, httpx.HTTPStatusError):
        handle_api_error(e.response.status_code, e.response.text)
    else:
        print(f"\n{R}An unexpected error occurred: {e}{R}\n")

def stream_openai_compatible(url, headers, payload):
    full = ""
    with httpx.stream("POST", url, headers=headers, json=payload, timeout=60, follow_redirects=True) as r:
        if r.status_code != 200:
            handle_api_error(r.status_code, r.read().decode())
            if r.status_code in [429, 500, 502, 503, 504]:
                raise httpx.HTTPStatusError("Retryable error", request=r.request, response=r)
            return ""
        
        for line in r.iter_lines():
            line = line.strip()
            if not line or line == "data: [DONE]": continue
            
            if line.startswith("data:"):
                try:
                    data = line[5:].strip()
                    chunk = json.loads(data)
                    if chunk.get('choices'):
                        delta = chunk['choices'][0].get('delta', {}).get('content', '')
                        if delta:
                            print(delta, end='', flush=True)
                            full += delta
                except json.JSONDecodeError: continue
            else:
                try:
                    chunk = json.loads(line)
                    if chunk.get('choices'):
                        content = chunk['choices'][0].get('message', {}).get('content', '')
                        if content:
                            print(content, end='', flush=True)
                            full += content
                    elif chunk.get('error'):
                        handle_api_error(r.status_code, line)
                except json.JSONDecodeError: continue
    return full

def stream_gemini(url, key, msgs):
    full = ""
    contents = []
    for m in msgs:
        role = "user" if m["role"] == "user" else "model"
        if m["role"] == "system": continue
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    
    full_url = f"{url}?alt=sse&key={key}"
    payload = {"contents": contents}
    
    with httpx.stream("POST", full_url, json=payload, timeout=60, follow_redirects=True) as r:
        if r.status_code != 200:
            handle_api_error(r.status_code, r.read().decode())
            if r.status_code in [429, 500, 502, 503, 504]:
                raise httpx.HTTPStatusError("Retryable error", request=r.request, response=r)
            return ""
            
        for line in r.iter_lines():
            if not line: continue
            try:
                line = line.strip()
                if line.startswith("data:"):
                    line = line[5:].strip()
                
                line = line.lstrip(',[').rstrip(',]')
                if not line: continue
                
                chunk = json.loads(line)
                candidates = chunk.get('candidates', [])
                if candidates:
                    text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                    if text:
                        print(text, end='', flush=True)
                        full += text
                elif chunk.get('error'):
                    handle_api_error(r.status_code, line)
            except (json.JSONDecodeError, KeyError, IndexError): continue
    return full

def execute_with_retry(func, *args, **kwargs):
    """Executes a function with exponential backoff retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
            if attempt == MAX_RETRIES - 1:
                print(f"{R}Maximum retries reached. Failing.{R}")
                return ""
            
            delay = BASE_BACKOFF_DELAY * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
            continue
        except Exception as e:
            handle_exception(e)
            return ""
    return ""

def main():
    load_env()
    parser = argparse.ArgumentParser(description="Multi-Provider CLI Chatbot")
    parser.add_argument("--provider", choices=["nvidia", "openrouter", "gemini"], default="nvidia", help="AI provider to use")
    args = parser.parse_args()

    cfg = get_config(args.provider)
    key = os.getenv(cfg["key_env"])
    if not key: return print(f"Error: {cfg['key_env']} not found in .env")

    print(f'{Y}--- CLI Chatbot ({args.provider.upper()}) ---{R}')
    print("Type 'exit' or 'quit' to end.\n")

    msgs = [{"role": "system", "content": "You are a helpful assistant."}]
    total_tokens = 0
    
    while True:
        try:
            u = input(f'{G}You:{R} ').strip()
            if u.lower() in {'exit', 'quit'}: break
            if not u: continue

            u_tokens = count_tokens(u)
            msgs.append({"role": "user", "content": u})
            print(f'{B}AI:{R} ', end='', flush=True)
            
            if args.provider == "gemini":
                full = execute_with_retry(stream_gemini, cfg["url"], key, msgs)
            else:
                payload = {"model": cfg["model"], "messages": msgs, "stream": True}
                full = execute_with_retry(stream_openai_compatible, cfg["url"], cfg.get("headers")(key), payload)
            
            if full:
                a_tokens = count_tokens(full)
                total_tokens += (u_tokens + a_tokens)
                print(f"\n{C}[Tokens: {u_tokens} user, {a_tokens} ai, {total_tokens} total]{R}\n")
                msgs.append({"role": "assistant", "content": full})
            else:
                print("\n")

        except (KeyboardInterrupt, EOFError): break
        except Exception as e: print(f'\nError: {e}\n')

if __name__ == '__main__': main()

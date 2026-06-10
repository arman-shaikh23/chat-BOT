import os, json, httpx, pathlib, argparse, sys

# Terminal Colors
G, B, R, Y = '\033[92m', '\033[94m', '\033[0m', '\033[93m'

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

def stream_openai_compatible(url, headers, payload):
    full = ""
    try:
        with httpx.stream("POST", url, headers=headers, json=payload, timeout=60, follow_redirects=True) as r:
            if r.status_code != 200:
                # Read the body to see the error message
                error_body = r.read().decode()
                print(f"\n{R}Error {r.status_code}: {error_body}{R}\n")
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
                    # Might be a full JSON response if streaming failed or wasn't supported
                    try:
                        chunk = json.loads(line)
                        if chunk.get('choices'):
                            content = chunk['choices'][0].get('message', {}).get('content', '')
                            if content:
                                print(content, end='', flush=True)
                                full += content
                        elif chunk.get('error'):
                            print(f"\n{R}API Error: {chunk['error']}{R}\n")
                    except json.JSONDecodeError: continue
    except Exception as e:
        print(f"\n{R}Connection Error: {e}{R}\n")
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
    
    try:
        with httpx.stream("POST", full_url, json=payload, timeout=60, follow_redirects=True) as r:
            if r.status_code != 200:
                error_body = r.read().decode()
                print(f"\n{R}Error {r.status_code}: {error_body}{R}\n")
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
                except (json.JSONDecodeError, KeyError, IndexError): continue
    except Exception as e:
        print(f"\n{R}Connection Error: {e}{R}\n")
    return full

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
    
    while True:
        try:
            u = input(f'{G}You:{R} ').strip()
            if u.lower() in {'exit', 'quit'}: break
            if not u: continue

            msgs.append({"role": "user", "content": u})
            print(f'{B}AI:{R} ', end='', flush=True)
            
            if args.provider == "gemini":
                full = stream_gemini(cfg["url"], key, msgs)
            else:
                payload = {"model": cfg["model"], "messages": msgs, "stream": True}
                full = stream_openai_compatible(cfg["url"], cfg.get("headers")(key), payload)
            
            print("\n")
            msgs.append({"role": "assistant", "content": full})

        except (KeyboardInterrupt, EOFError): break
        except Exception as e: print(f'\nError: {e}\n')

if __name__ == '__main__': main()

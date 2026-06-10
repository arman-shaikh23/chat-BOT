import os, json, httpx, pathlib

# Terminal Colors
G, B, R = '\033[92m', '\033[94m', '\033[0m'

def load_env():
    """Loads environment variables from .env file."""
    p = pathlib.Path('.env')
    if p.exists():
        for line in p.read_text(encoding='utf-8').splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

def main():
    load_env()
    key = os.getenv("NVIDIA_API_KEY")
    if not key: return print("Error: NVIDIA_API_KEY not found in .env")

    print(f'--- NVIDIA NIM CLI Chatbot (Llama 3.1) ---')
    print("Type 'exit' or 'quit' to end.\n")

    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    msgs = [{"role": "system", "content": "You are a helpful assistant."}]
    
    while True:
        try:
            u = input(f'{G}You:{R} ').strip()
            if u.lower() in {'exit', 'quit'}: break
            if not u: continue

            msgs.append({"role": "user", "content": u})
            print(f'{B}AI:{R} ', end='', flush=True)
            full = ""
            
            with httpx.stream("POST", url, headers={"Authorization": f"Bearer {key}"},
                             json={"model": "meta/llama-3.1-8b-instruct", "messages": msgs, "stream": True},
                             timeout=60) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line.startswith("data: ") and "[DONE]" not in line:
                        try:
                            chunk = json.loads(line[6:])
                            if chunk.get('choices'):
                                delta = chunk['choices'][0].get('delta', {}).get('content', '')
                                if delta:
                                    print(delta, end='', flush=True)
                                    full += delta
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
            
            print("\n")
            msgs.append({"role": "assistant", "content": full})

        except (KeyboardInterrupt, EOFError): break
        except Exception as e: print(f'\nError: {e}\n')

if __name__ == '__main__': main()

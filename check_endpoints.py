import requests

urls = [
    "https://sgtm.messerattach.com/healthz",
    "https://messerattach.com/metrics/healthz",
    "https://messerattach.com/metrics/data"
]

def check_url(url):
    print(f"\n--- Checking {url} ---")
    try:
        r = requests.get(url, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {r.headers.get('Content-Type')}")
        print(f"Server: {r.headers.get('Server')}")
        sample = r.text[:200].replace('\n', ' ')
        print(f"Body Sample: {sample}")
        
    except Exception as e:
        print(f"Error: {e}")

for u in urls:
    check_url(u)

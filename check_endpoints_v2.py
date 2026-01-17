import urllib.request
import urllib.error

urls = [
    "https://sgtm.messerattach.com/healthz",
    "https://messerattach.com/metrics/healthz",
    "https://messerattach.com/metrics/data"
]

def check_url(url):
    print(f"\n--- Checking {url} ---")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as r:
            print(f"Status: {r.status}")
            print(f"Content-Type: {r.headers.get('Content-Type')}")
            sample = r.read().decode('utf-8', errors='ignore')[:200].replace('\n', ' ')
            print(f"Body Sample: {sample}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code}")
    except Exception as e:
        print(f"Error: {e}")

for u in urls:
    check_url(u)

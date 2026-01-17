import urllib.request
import urllib.error

url = "https://sgtm.messerattach.com/data"

print(f"\n--- Checking {url} ---")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as r:
        print(f"Status: {r.status}")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
except Exception as e:
    print(f"Error: {e}")

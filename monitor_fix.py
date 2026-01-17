import time
import urllib.request
import urllib.error
import sys

URL = "https://messerattach.com/metrics/data"
EXPECTED_STATUS = 200

def check_status():
    print(f"Monitoring {URL} for fix...")
    start_time = time.time()
    
    # Run for 2 minutes or until fixed
    while time.time() - start_time < 120:
        try:
            req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0 (ValidationScript)'})
            with urllib.request.urlopen(req) as r:
                status = r.status
                print(f"[{time.strftime('%H:%M:%S')}] Status: {status}")
                
                if status == EXPECTED_STATUS:
                    print("\n✅ SUCCESS! The endpoint is returning 200 OK.")
                    print("The Cloudflare Worker is now correctly proxying requests.")
                    return True
                else:
                    print(f"⚠️ Still returning {status}...")
                    
        except urllib.error.HTTPError as e:
            print(f"[{time.strftime('%H:%M:%S')}] Status: {e.code} (Still failing)")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")
            
        time.sleep(5)
    
    print("\n⏳ Timeout. Please make the changes in Cloudflare and run this script again.")
    return False

if __name__ == "__main__":
    check_status()

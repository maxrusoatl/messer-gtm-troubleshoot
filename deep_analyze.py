import json
import csv
import re
from collections import Counter

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"
sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_sgtm_messerattach_com_2026_01_15.json"
logs_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\stape io messer logs.csv"

def analyze_web_gtm():
    print("\n--- Web GTM Event Analysis ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            containers = data.get('data', {}).get('containers', [])
            
            for c in containers:
                pid = c.get('publicId', 'unknown')
                print(f"Container: {pid}")
                
                messages = c.get('messages', [])
                print(f"  Messages: {len(messages)}")
                
                for msg in messages:
                    # Look for view_item
                    msg_str = json.dumps(msg)
                    if 'view_item' in msg_str:
                        # Extract event name precisely if possible
                        event_name = msg.get('eventName', 'N/A')
                        print(f"  Found '{event_name}' event. Index: {msg.get('index')}")
                        
                        # Check for tag firings associated with this message
                        # Usually 'tagsFired' isn't in the message directly in some exports, 
                        # but let's check basic structure if Tags are mentioned.
                        # Actually TA recordings separate tags from messages. 
                        # 'tagsFired' was a top level key in the snippet we saw!
                
                # Check tagsFired if present in container
                tags_fired = c.get('tagsFired', {})
                # tagsFired is often map { messageIndex: [tags] }
                print(f"  Tags Fired Map Keys (Message Indexes): {len(tags_fired)}")
                
    except Exception as e:
        print(f"Error Web GTM: {e}")

def analyze_sgtm():
    print("\n--- sGTM Event Analysis ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            containers = data.get('data', {}).get('containers', [])
            
            for c in containers:
                pid = c.get('publicId', 'unknown')
                print(f"Container: {pid}")
                messages = c.get('messages', []) # sGTM usually has request logs as messages
                for msg in messages:
                    if 'view_item' in json.dumps(msg):
                        print("  Found view_item in sGTM message.")
                        
    except Exception as e:
        print(f"Error sGTM: {e}")

def analyze_logs():
    print("\n--- Stape Logs URL Analysis ---")
    unique_urls = Counter()
    
    try:
        with open(logs_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                url = row.get('Request Url', '')
                # Simplify URL to base path to group them
                # Remove query params
                base_url = url.split('?')[0]
                unique_urls[base_url] += 1
                count += 1
                
            print(f"Total Log Entries: {count}")
            print("Unique Request Paths (Top 20):")
            for url, cnt in unique_urls.most_common(20):
                print(f"  {cnt}: {url}")
                
    except Exception as e:
        print(f"Error Logs: {e}")

if __name__ == "__main__":
    analyze_web_gtm()
    analyze_sgtm()
    analyze_logs()

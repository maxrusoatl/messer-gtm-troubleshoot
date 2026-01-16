import json
import csv
import sys
import re

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"
sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_sgtm_messerattach_com_2026_01_15.json"
logs_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\stape io messer logs.csv"

def parse_web_gtm():
    print("--- Web GTM Analysis ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Structure of Tag Assistant JSON usually has 'messages' or 'log'
        # Let's inspect keys
        # print(f"Keys: {list(data.keys())}")
        
        # Usually data is in 'messages' list
        messages = data.get('messages', [])
        if not messages and 'data' in data:
             messages = data['data'].get('messages', [])
        
        print(f"Total messages: {len(messages)}")
        
        found_view_item = False
        for msg in messages:
            # Check for data layer events or tags fired
            # Structure varies. Often has 'messageType', 'content'
            # Or data layer pushes
            
            # Simple check for 'view_item' in string repr of message for now, then drill down
            msg_str = json.dumps(msg)
            if 'view_item' in msg_str:
                # print(f"Found view_item in message: {msg_str[:200]}...")
                pass

            # Look for outgoing requests to "messerattach.com/metrics"
            if 'messerattach.com/metrics' in msg_str:
                 print(f"Found outgoing request to metrics: {msg_str[:200]}...")

    except Exception as e:
        print(f"Error parsing Web GTM: {e}")

def parse_sgtm():
    print("\n--- sGTM Analysis ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Check for event data
        # sGTM export might be different. 
        # Look for 'events' or processed requests.
        
        # 'data' key usually holds the content
        content = data.get('data', {})
        
        # Looking for processed events
        # Sometimes under 'eventData' or similar
        # Let's look for known keys from previous view
        # 'debugContext', 'domainDetails' were seen.
        
        # Maybe 'log' or 'requests'?
        # The file viewed earlier had 'messages': [], 'tagsFired': {}
        # But 'tagsFired' was empty in the snippet.
        
        # If the recording captured events, they should be in 'messages' or similar.
        messages = content.get('messages', [])
        print(f"Total sGTM messages: {len(messages)}")
        
        for msg in messages:
             if 'view_item' in json.dumps(msg):
                 print("Found view_item in sGTM message")

    except Exception as e:
        print(f"Error parsing sGTM: {e}")

def parse_logs():
    print("\n--- Stape Logs Analysis ---")
    try:
        with open(logs_path, 'r', encoding='utf-8') as f:
            # The CSV seems to have quoted multiline fields. csv module handles this.
            reader = csv.DictReader(f)
            
            count = 0
            found_data = False
            for row in reader:
                url = row.get('Request Url', '')
                if '/data' in url:
                    print(f"Found /data request: {url} - Status: {row.get('Response Status Code')}")
                    found_data = True
                    # Print log data if interesting
                    if 'Log Data' in row:
                        host = re.search(r'RequestHost: (.*)', row['Log Data'])
                        if host:
                            print(f"  Host: {host.group(1)}")
                
                if 'view_item' in str(row):
                     print(f"Found view_item in logs: {row}")
                
                count += 1
            
            print(f"Scanned {count} log entries.")
            if not found_data:
                print("No /data requests found in logs.")

    except Exception as e:
        print(f"Error parsing logs: {e}")

if __name__ == "__main__":
    parse_web_gtm()
    parse_sgtm()
    parse_logs()

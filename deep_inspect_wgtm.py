import json

path_w = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_messerattach_com_2026_01_15.json"

def inspect_data(path):
    print(f"--- Inspecting DATA inside {path} ---")
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        data = content.get('data', {})
        print(f"Data Keys: {data.keys()}")
        
        # Check logs or events
        if 'events' in data:
            print(f"Events list length: {len(data['events'])}")
            if len(data['events']) > 0:
                print(f"Sample Event: {data['events'][0].keys()}")
        
        if 'logs' in data:
             print(f"Logs list length: {len(data['logs'])}")

inspect_data(path_w)

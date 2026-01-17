import json

path_w = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_messerattach_com_2026_01_15.json"
path_s = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_sgtm_messerattach_com_2026_01_15.json"

def inspect(path, name):
    print(f"--- Inspecting {name} ---")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                print(f"Root is list, length: {len(data)}")
                print(f"Sample keys: {data[0].keys() if len(data)>0 else 'Empty'}")
            elif isinstance(data, dict):
                print(f"Root is dict, keys: {data.keys()}")
                if 'logs' in data:
                    print(f"Logs length: {len(data['logs'])}")
                if 'events' in data:
                    print(f"Events length: {len(data['events'])}")
    except Exception as e:
        print(f"Error: {e}")

inspect(path_w, "wGTM")
inspect(path_s, "sGTM")

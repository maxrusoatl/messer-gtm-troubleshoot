import json
import csv

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"
sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_sgtm_messerattach_com_2026_01_15.json"

def inspect_json():
    print("--- Web GTM Keys ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Top keys: {list(data.keys())}")
            if 'data' in data:
                print(f"Data keys: {list(data['data'].keys())}")
                if 'messages' in data['data']:
                     print(f"Messages type: {type(data['data']['messages'])}")
                if 'logs' in data['data']:
                     print(f"Logs len: {len(data['data']['logs'])}")
            
            # recursive search for large lists which might hold events
            for k, v in data.items():
                if isinstance(v, list):
                    print(f"List '{k}' length: {len(v)}")
    except Exception as e:
        print(f"Error Web GTM: {e}")

    print("\n--- sGTM Keys ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Top keys: {list(data.keys())}")
            if 'data' in data:
                 print(f"Data keys: {list(data['data'].keys())}")
    except Exception as e:
        print(f"Error sGTM: {e}")

if __name__ == "__main__":
    inspect_json()

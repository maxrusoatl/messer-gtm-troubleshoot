import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"

def inspect_data_tag_firings():
    print("--- Inspecting Data Tag Firings ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            containers = data.get('data', {}).get('containers', [])
            
            for c in containers:
                pid = c.get('publicId')
                tags_fired = c.get('tagsFired', {})
                
                # Check directly for 'Data Tag' or tag ID 310 if keys are IDs
                # The previous output showed Names as keys.
                
                dt_info = tags_fired.get('Data Tag')
                if dt_info:
                    print(f"\nContainer: {pid}")
                    print(f"Data Tag Firing Info (Type: {type(dt_info)}):")
                    # It might be a list of firings
                    if isinstance(dt_info, list):
                        print(f"Count: {len(dt_info)}")
                        for i, firing in enumerate(dt_info):
                            print(f"  Firing {i}: Keys: {list(firing.keys())}")
                            # relevant keys might be 'fireStatus', 'messageIndex', 'tagModel'
                            idx = firing.get('messageIndex')
                            status = firing.get('fireStatus')
                            print(f"    Message Index: {idx}, Status: {status}")
                            
                            # Inspect tag data/requestURL if present
                            # Maybe in 'tagModel' -> 'parameters'?
                    else:
                        print("Structure is not a list?")
                        print(json.dumps(dt_info, indent=2))
                else:
                    print(f"\nContainer: {pid} - 'Data Tag' key not found in tagsFired.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_data_tag_firings()

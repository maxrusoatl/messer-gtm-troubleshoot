import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"

def inspect_datatag_details():
    print("--- Inspecting Data Tag Details ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            containers = data.get('data', {}).get('containers', [])
            
            for c in containers:
                tags_fired = c.get('tagsFired', {})
                dt_info = tags_fired.get('Data Tag')
                
                if dt_info:
                    print(f"Container: {c.get('publicId')}")
                    # Look at the first firing detail
                    first = dt_info[0]
                    
                    print(f"Event Name: {first.get('eventName')}")
                    
                    # tagInfo
                    tinfo = first.get('tagInfo', {})
                    # Inspect tagInfo
                    print(f"Tag Info: {json.dumps(tinfo, indent=2)}")
                    
                    # Search for 'https' in the string dump of the firing
                    s = json.dumps(first)
                    if "https://" in s:
                        print("\nFound URL in firing object:")
                        # Extract rudimentary URLs
                        import re
                        urls = re.findall(r'https?://[^\s"\'<>]+', s)
                        for u in urls:
                            print(f"  {u}")
                    else:
                        print("\nNo URL found in firing object.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_datatag_details()

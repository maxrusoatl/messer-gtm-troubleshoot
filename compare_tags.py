import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"

def compare_google_tag():
    print("--- Comparing Google Tag vs Data Tag ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            c = data.get('data', {}).get('containers', [])[0]
            
            tags_fired = c.get('tagsFired', {})
            gt_firings = tags_fired.get('Google Tag', [])
            dt_firings = tags_fired.get('Data Tag', [])
            
            print(f"Google Tag Firings: {len(gt_firings)}")
            for f in gt_firings:
                print(f"  GT Firing Msg Index: {f.get('messageIndex')}, Status: {f.get('fireStatus')}")
                
            print(f"Data Tag Firings: {len(dt_firings)}")
            for f in dt_firings:
                 print(f"  DT Firing Msg Index: {f.get('messageIndex')}, Status: {f.get('fireStatus')}")

            # Check Trigger for Google Tag
            # We need to find the Google Tag ID first (from export, known as GT-NS9Z5FWG? No, that's the ID.
            # In tagsFired it's by Name.
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compare_google_tag()

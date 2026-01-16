import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"

def check_any_fired_tags():
    print("--- Any Fired Tags Check ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            containers = data.get('data', {}).get('containers', [])
            
            for c in containers:
                pid = c.get('publicId', 'unknown')
                print(f"\nContainer: {pid}")
                tags_fired = c.get('tagsFired', {})
                print(f"  Total events with tags fired: {len(tags_fired)}")
                
                # List the indexes that fired tags
                print(f"  Indexes with fired tags: {list(tags_fired.keys())}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_any_fired_tags()

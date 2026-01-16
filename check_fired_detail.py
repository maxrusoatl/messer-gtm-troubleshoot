import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"

def check_fired_tags_detail():
    print("--- Fired Tags Detail for view_item ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            containers = data.get('data', {}).get('containers', [])
            
            for c in containers:
                pid = c.get('publicId', 'unknown')
                print(f"\nContainer: {pid}")
                messages = c.get('messages', [])
                tags_fired = c.get('tagsFired', {})
                
                for msg in messages:
                    if 'view_item' in json.dumps(msg):
                        idx = str(msg.get('index'))
                        event = msg.get('eventName')
                        print(f"  Event: {event} (Index {idx})")
                        
                        fired = tags_fired.get(idx, [])
                        if fired:
                            print(f"    Tags fired ({len(fired)}):")
                            for t in fired:
                                if isinstance(t, dict):
                                    tid = t.get('id') or t.get('tagId')
                                    tname = t.get('name', 'Unknown')
                                    print(f"      - ID: {tid}, Name: {tname}, Status: {t.get('status')}")
                                else:
                                    print(f"      - {t}")
                        else:
                            print("    No tags fired.")
                            
                        # Limit to first few instances
                        # break 

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_fired_tags_detail()

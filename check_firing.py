import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"

def check_tag_firing():
    print("--- Web GTM Tag Firing Check ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Find the correct container (Web GTM)
            # We suspect C0 (GTM-K3CQBMZ9) is labeled server but contains browser events? 
            # Or C1? The events were in both.
            # Let's check both for Tag 310.
            
            containers = data.get('data', {}).get('containers', [])
            
            target_tag_id = "310" # Data Tag
            
            for c in containers:
                pid = c.get('publicId', 'unknown')
                print(f"\nContainer: {pid}")
                
                messages = c.get('messages', [])
                tags_fired = c.get('tagsFired', {}) # Map: messageIndex -> list of tags
                
                for msg in messages:
                    msg_str = json.dumps(msg)
                    if 'view_item' in msg_str:
                        idx = str(msg.get('index'))
                        event_name = msg.get('eventName', 'N/A')
                        print(f"  Event '{event_name}' (Index {idx})")
                        
                        # Check fired tags for this event
                        fired = tags_fired.get(idx, [])
                        # fired is likely a list of Tag objects or IDs
                        # Let's inspect the structure of a fired tag entry
                        
                        data_tag_fired = False
                        if fired:
                            # print(f"    Tags fired count: {len(fired)}")
                            for t in fired:
                                # t might be just ID or object
                                # If object, look for 'id' or 'tagId'
                                t_id = "N/A"
                                if isinstance(t, dict):
                                    t_id = str(t.get('id') or t.get('tagId') or 'unknown')
                                else:
                                    t_id = str(t)
                                
                                if t_id == target_tag_id:
                                    data_tag_fired = True
                                    print(f"    SUCCESS: Data Tag ({target_tag_id}) fired!")
                                    # If possible, print tag status/data
                                    break
                        else:
                            print("    No tags fired for this event.")
                            
                        if not data_tag_fired:
                             print(f"    Data Tag ({target_tag_id}) did NOT fire.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tag_firing()

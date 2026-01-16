import json

json_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\GTM-MNRP4PF_workspace253.json"

def inspect_tag_310():
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Navigate to container -> tag
            tags = data.get('containerVersion', {}).get('tag', [])
            triggers = data.get('containerVersion', {}).get('trigger', [])
            
            # Create trigger lookup
            trigger_map = {t['triggerId']: t for t in triggers}
            
            target_tag = None
            for t in tags:
                if t.get('tagId') == "310":
                    target_tag = t
                    break
            
            if target_tag:
                print("--- Tag 310 (Data Tag) ---")
                print(json.dumps(target_tag, indent=2))
                
                print("\n--- Firing Triggers ---")
                firing_ids = target_tag.get('firingTriggerId', [])
                for fid in firing_ids:
                    trig = trigger_map.get(fid)
                    if trig:
                        print(f"Trigger {fid}:")
                        print(json.dumps(trig, indent=2))
                    else:
                        print(f"Trigger {fid} not found!")

                print("\n--- Blocking Triggers ---")
                blocking_ids = target_tag.get('blockingTriggerId', [])
                for bid in blocking_ids:
                    trig = trigger_map.get(bid)
                    if trig:
                        print(f"Trigger {bid}:")
                        print(json.dumps(trig, indent=2))
                    else:
                        print(f"Trigger {bid} not found!")
                        
            else:
                print("Tag 310 not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_tag_310()

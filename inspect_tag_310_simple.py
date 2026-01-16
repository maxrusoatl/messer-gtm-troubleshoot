import json

json_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\GTM-MNRP4PF_workspace253.json"

def inspect_tag_310_simple():
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            tags = data.get('containerVersion', {}).get('tag', [])
            triggers = data.get('containerVersion', {}).get('trigger', [])
            trigger_map = {t['triggerId']: t for t in triggers}
            
            target_tag = None
            for t in tags:
                if t.get('tagId') == "310":
                    target_tag = t
                    break
            
            if target_tag:
                print(f"Tag: {target_tag.get('name')} (ID: {target_tag.get('tagId')})")
                print(f"Consent Settings: {target_tag.get('consentSettings')}")
                
                print("Firing Triggers:")
                for fid in target_tag.get('firingTriggerId', []):
                    t = trigger_map.get(fid)
                    if t:
                        print(f" - ID: {fid}, Name: {t.get('name')}, Type: {t.get('type')}")
                        if 'customEventFilter' in t:
                             print(f"   Filters: {json.dumps(t['customEventFilter'])}")

                print("Blocking Triggers:")
                for bid in target_tag.get('blockingTriggerId', []):
                    t = trigger_map.get(bid)
                    if t:
                        print(f" - ID: {bid}, Name: {t.get('name')}, Type: {t.get('type')}")
            else:
                print("Tag not found")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_tag_310_simple()

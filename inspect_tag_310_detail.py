import json

wgtm_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\GTM-MNRP4PF_workspace253.json"

def inspect_tag_310_detail(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    tags = data.get('containerVersion', {}).get('tag', [])
    triggers = data.get('containerVersion', {}).get('trigger', [])
    
    for tag in tags:
        if tag['tagId'] == '310':
            print("--- Tag 310 Full Dump ---")
            print(json.dumps(tag, indent=2))
            
            # Check for blocking triggers
            if 'blockingTriggerId' in tag:
                print("\nBlocking Trigger IDs found:", tag['blockingTriggerId'])
            
            # Check firing triggers lookup
            f_ids = tag.get('firingTriggerId', [])
            for t_id in f_ids:
                for t in triggers:
                    if t['triggerId'] == t_id:
                        print(f"\n--- Firing Trigger {t_id} Dump ---")
                        print(json.dumps(t, indent=2))

inspect_tag_310_detail(wgtm_path)

import json

wgtm_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\GTM-MNRP4PF_workspace253.json"

def inspect_tag_310(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    container = data.get('containerVersion', {}).get('container', {})
    tags = data.get('containerVersion', {}).get('tag', [])
    triggers = data.get('containerVersion', {}).get('trigger', [])
    variables = data.get('containerVersion', {}).get('variable', [])
    
    # 1. Find Tag 310 Trigger
    trigger_ids = []
    for tag in tags:
        if tag['tagId'] == '310':
            print(f"Tag 310 Found: {tag['name']}")
            print(f"Firing Trigger IDs: {tag.get('firingTriggerId')}")
            trigger_ids = tag.get('firingTriggerId', [])
            break
            
    # 2. Inspect Triggers
    print("\nTrigger Details:")
    for t in triggers:
        if t['triggerId'] in trigger_ids:
            print(f"Trigger {t['triggerId']}: {t['name']} (Type: {t['type']})")
            if 'customEventFilter' in t:
                print(f"  - Custom Event Filter: {t['customEventFilter']}")
            if 'filter' in t:
                print(f"  - Filters: {t['filter']}")
            if 'autoEventFilter' in t:
                 print(f"  - Auto Event Filter: {t['autoEventFilter']}")

inspect_tag_310(wgtm_path)

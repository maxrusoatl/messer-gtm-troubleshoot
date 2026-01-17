import json

# Paths
wgtm_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_messerattach_com_2026_01_15.json"
sgtm_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_sgtm_messerattach_com_2026_01_15.json"

# IDs
WGTM_ID = "GTM-MNRP4PF"
SGTM_ID = "GTM-K3CQBMZ9"
DATA_TAG_ID = "310" # wGTM Data Tag
SGTM_GA4_TAG_ID = "16" # sGTM GA4 Advanced
SGTM_ADS_CHECKOUT = "8"
SGTM_ADS_ATC = "25"
SGTM_ADS_PURCHASE = "55" # Wait, 55 was CAPI Purchase. Ads Purchase is 46? Need to re-check inventory.
# From Step 1 Output:
# Tag 8: Ads Checkout
# Tag 25: Ads ATC
# Tag 46: Conversion Linker (Wait, let's re-verify Ads Purchase tag ID from file if possible or assume logic)
# Actually, the python output for sGTM inventory showed:
# Tag 55: FB CAPI Purchase
# Tag 8: Ads Checkout
# Tag 25: Ads ATC
# Tag 46 was Conversion Linker? 
# Wait, the output for sGTM said "Tag: Google Ads Conversion Tracking - Purchase (Type: Google Ads Conversion)" but didn't print ID?
# Let's trust the names for now.

def analyze_wgtm(path):
    print("\n=== Analying wGTM Recording ===")
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        
    containers = content.get('data', {}).get('containers', [])
    target_container = None
    for c in containers:
        if c.get('publicId') == WGTM_ID:
            target_container = c
            break
            
    if not target_container:
        print(f"Container {WGTM_ID} not found in recording.")
        for c in containers:
            print(f"Found container: {c.get('publicId')}")
        return

    print(f"Found wGTM Container: {WGTM_ID}")
    
    # Iterate messages (timeline)
    messages = target_container.get('messages', [])
    print(f"Total Messages: {len(messages)}")
    
    events_of_interest = ['view_item', 'add_to_cart', 'begin_checkout', 'purchase']
    
    for msg in messages:
        # Check for dataLayer push
        msg_data = msg.get('messageType')
        event_name = "Unknown"
        event_data = {}
        
        # Extract Event Name from Data Layer
        # Usually in 'dataLayer' key or similar
        # Tag Assistant structure is tricky. 'event' key inside msg?
        # Let's look at 'eventName' if present.
        
        event_name = msg.get('eventName')
        
        if event_name in events_of_interest:
            print(f"\n[EVENT] {event_name} (Msg Index: {msg.get('index')})")
            print(f"  - Message Keys: {msg.keys()}")
            # Print sample data layer content if available
            # Typically 'message' key holds the DL push
            if 'message' in msg:
                 print(f"  - DL Push: {str(msg['message'])[:200]}")
            
            # Check Data Layer Payload
            # We need to find the data model at this step.
            # Usually implied, or we look at variables.
            
            # Check Tags Fired
            tags = msg.get('tagInfo', []) # Try tagInfo
            # If tagInfo is not a list, maybe it's a dict?
            if isinstance(tags, dict):
                 # Sometimes under 'firedTags', 'notFiredTags'
                 print(f"  - TagInfo Keys: {tags.keys()}")
                 # Flatten for search
                 flat_tags = []
                 for k in tags:
                     if isinstance(tags[k], list):
                         flat_tags.extend(tags[k])
                 tags = flat_tags
            
            if len(tags) > 0:
                print(f"  - Sample TagInfo Item keys: {tags[0].keys()}")
                print(f"  - Sample TagInfo Item: {str(tags[0])[:200]}") # Print first 200 chars
            
            print(f"  - Total TagsEvaluated: {len(tags)}")
            found_310 = False
            tag_names = []
            for tag in tags:
                # Debug keys for first tag
                if len(tag_names) == 0:
                     print(f"  - First Tag Keys: {tag.keys()}")
                
                t_name = tag.get('name', 'Unknown')
                # Check for status
                status_keys = [k for k in tag.keys() if 'status' in k.lower() or 'fire' in k.lower()]
                status_val = "Unknown"
                if status_keys:
                    status_val = f"{status_keys[0]}:{tag[status_keys[0]]}"
                
                tag_names.append(f"{t_name} ({status_val})")
                
                if "Data Tag" in t_name or t_name == "Data Tag":
                    print(f"  - FOUND Data Tag by Name: {t_name}, Status: {status_val}")
                    found_310 = True
            
            print(f"  - Tags Evaluated (First 5): {', '.join(tag_names[:5])}...")
            
            # Inspect logInfo
            log_info = msg.get('logInfo')
            if log_info:
                print(f"  - LogInfo Keys: {log_info.keys()}")
                print(f"  - LogInfo Sample: {str(log_info)[:300]}")
            
            if not found_310:
                 print("  - WARNING: Data Tag was NOT found in the evaluation list for this event.")

def analyze_sgtm(path):
    print("\n=== Analying sGTM Recording ===")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)
    except:
        print("Could not load sGTM recording")
        return

    containers = content.get('data', {}).get('containers', [])
    target_container = None
    for c in containers:
        if c.get('publicId') == SGTM_ID:
            target_container = c
            break
            
    if not target_container:
        print(f"Container {SGTM_ID} not found in sGTM recording.")
        for c in containers:
             print(f"Found container: {c.get('publicId')}")
        return

    print(f"Found sGTM Container: {SGTM_ID}")
    
    messages = target_container.get('messages', [])
    print(f"Total Messages: {len(messages)}")
    
    for msg in messages:
        # sGTM structure: incoming requests show up as events?
        # Look for 'eventName'
        evt = msg.get('eventName')
        if evt:
            print(f"\n[sGTM EVENT] {evt}")
            
            # Check Client
            # Usually in 'request' details or similar
            
            # Check Tags Fired
            tags = msg.get('tags', [])
            for tag in tags:
                # format might be different. name? 
                name = tag.get('tagName')
                status = tag.get('status')
                if status == 'fired': # check keywords
                    if 'GA4' in name:
                        print(f"  - GA4 Tag Fired: {name}")
                    if 'Ads' in name:
                        print(f"  - Ads Tag Fired: {name}")

analyze_wgtm(wgtm_path)
analyze_sgtm(sgtm_path)

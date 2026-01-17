import json
import os
import sys

# Paths
wgtm_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\GTM-MNRP4PF_workspace253.json"
sgtm_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\GTM-K3CQBMZ9_workspace40.json"
wgtm_recording_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_messerattach_com_2026_01_15.json"
sgtm_recording_path = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_sgtm_messerattach_com_2026_01_15.json"

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def extract_wgtm_inventory(data):
    print("--- wGTM Inventory ---")
    container = data.get('containerVersion', {})
    tags = container.get('tag', [])
    variables = container.get('variable', [])
    
    # helper to find variable value
    def resolve_variable(name_or_id):
        # Implementation simplified, usually just looks up by name if {{}} or id
        return name_or_id

    for tag in tags:
        if tag['type'] == 'cvt_MBTSV': # Data Tag
            print(f"Tag: {tag['name']} (Type: Stape Data Tag)")
            for param in tag.get('parameter', []):
                if param['key'] == 'gtm_server_domain':
                    print(f"  - Server URL: {param['value']}")
                if param['key'] == 'event_name_custom':
                    print(f"  - Event Name: {param['value']}")
        
        if tag['type'] == 'googtag' or tag['type'] == 'gaawe': # GA4 Config or Event
            print(f"Tag: {tag['name']} (Type: GA4)")
            # Extract Measurement ID
            for param in tag.get('parameter', []):
                 if param['key'] == 'measurementId':
                     print(f"  - Measurement ID: {param['value']}")
        
        if tag['type'] == 'awct': # Google Ads Conversion
            print(f"Tag: {tag['name']} (Type: Google Ads)")
            for param in tag.get('parameter', []):
                 if param['key'] == 'conversionId':
                     print(f"  - ID: {param['value']}")
                 if param['key'] == 'conversionLabel':
                     print(f"  - Label: {param['value']}")

def extract_sgtm_inventory(data):
    print("\n--- sGTM Inventory ---")
    container = data.get('containerVersion', {})
    tags = container.get('tag', [])
    clients = container.get('client', []) # Actually triggers/variables/etc are different? Wait, clients are in 'client' key usually? 
    # In the JSON provided earlier, I saw 'template' for Client under customTemplate, but actual instances are tags? 
    # No, Clients are top level in containerVersion usually?
    # Checking the file content provided earlier... I didn't see a "client" array in the view_file output. 
    # It might be I missed it or it wasn't shown. Let's assume standard structure.
    
    # Actually, in the earlier view_file, I saw "Tag Manager" structure. 
    # Clients are usually under 'client' in the export JSON.
    
    for tag in tags:
        if tag['type'] == 'cvt_K8FK5': # GA4 Advanced
            print(f"Tag: {tag['name']} (Type: GA4 Advanced)")
            for param in tag.get('parameter', []):
                if param['key'] == 'measurementId':
                    print(f"  - Measurement ID: {param.get('value')}")
        
        if tag['type'] == 'sgtmadsct': # Google Ads Conversion
            print(f"Tag: {tag['name']} (Type: Google Ads Conversion)")
            for param in tag.get('parameter', []):
                if param['key'] == 'conversionId':
                    print(f"  - ID: {param.get('value')}")
                if param['key'] == 'conversionLabel':
                    print(f"  - Label: {param.get('value')}")

def analyze_recordings(wgtm_rec, sgtm_rec):
    print("\n--- Recording Analysis ---")
    # This is complex as structure varies.
    # We look for "events" list.
    
    # wGTM Events
    w_events = wgtm_rec.get('logs', []) # or 'events'
    # Actually TA JSON export structure: { "logs": [...], "summary": ... }
    
    # Find relevant events
    target_events = ['view_item', 'add_to_cart', 'begin_checkout', 'purchase']
    
    print(f"wGTM Log Count: {len(w_events)}")
    
    # Simple search for event names in wGTM logs
    # Note: Structure is usually a list of log entries. Each entry has 'message'.
    # Message can be "dataLayer.push".
    
    found_events = {}
    
    # Heuristic parsing of large JSON structure for TA
    # We will just print the pointers to events found
    
    pass

def main():
    wgtm = load_json(wgtm_path)
    if wgtm:
        extract_wgtm_inventory(wgtm)
        
    sgtm = load_json(sgtm_path)
    if sgtm:
        extract_sgtm_inventory(sgtm)

    # Recordings are too big/complex to blindly dump. 
    # I will inspect keys first in a separate check or use this script to just load them and print keys.
    
if __name__ == "__main__":
    main()

import json

sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\GTM-K3CQBMZ9_workspace40.json"

def analyze_sgtm_logic():
    print("--- sGTM Logic Audit ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            cv = data.get('containerVersion', {})
            
            # 1. Verify Data Client Path
            clients = cv.get('client', [])
            data_client_found = False
            for c in clients:
                if 'Data Client' in c.get('name', ''):
                    data_client_found = True
                    print(f"Client: {c.get('name')}")
                    # Path Settings often hidden in variable references or default
                    # We check parameters
                    print(f"  Params: {json.dumps(c.get('parameter', []), indent=2)}")
            
            if not data_client_found:
                print("CRITICAL: Data Client not found in sGTM export.")

            # 2. Analyze Triggers (When do tags fire?)
            triggers = cv.get('trigger', [])
            trigger_map = {t['triggerId']: t for t in triggers}
            
            # 3. Analyze Tags (What fires?)
            tags = cv.get('tag', [])
            print(f"\nTotal Tags: {len(tags)}")
            
            for t in tags:
                name = t.get('name')
                type = t.get('type')
                
                # We care about GA4, Ads, CAPI
                if type in ['sgtmadsct', 'cvt_K8FK5', 'cvt_5TP8W', 'sgtmadscl']:
                    print(f"\nTag: {name} ({type})")
                    
                    # Firing Triggers
                    firing = t.get('firingTriggerId', [])
                    for fid in firing:
                        trig = trigger_map.get(fid)
                        if trig:
                            print(f"  Trigger: {trig.get('name')} (Type: {trig.get('type')})")
                            # Check conditions
                            filters = trig.get('customEventFilter', [])
                            if filters:
                                print(f"    Filters: {json.dumps(filters)}")
                            # Check Event Name condition
                            # Usually in filter or main event name
                        else:
                            print(f"  Trigger {fid} missing")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_sgtm_logic()

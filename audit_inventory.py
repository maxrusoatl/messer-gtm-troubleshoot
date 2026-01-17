import json
import re

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\GTM-MNRP4PF_workspace253.json"
sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\GTM-K3CQBMZ9_workspace40.json"

def extract_from_container(path, label):
    print(f"\n--- Inventory: {label} ---")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            container = data.get('containerVersion', {}).get('container', {})
            cv = data.get('containerVersion', {})
            
            print(f"Container ID: {container.get('publicId')}")
            print(f"Version: {cv.get('containerVersionId')}")
            
            # Variables
            vars = cv.get('variable', [])
            print(f"Total Variables: {len(vars)}")
            
            # Find GA4 IDs
            ga4_ids = set()
            for v in vars:
                if v.get('type') == 'c' or 'ga4' in v.get('name', '').lower():
                   # simple heuristic, check value
                   val = v.get('parameter', [{}])[0].get('value', '')
                   if isinstance(val, str) and val.startswith('G-'):
                       ga4_ids.add(val)
            print(f"GA4 IDs found: {ga4_ids}")

            # Find Ads IDs
            ads_ids = set()
            for v in vars:
                # check for AW- or conversion ID keys
                val = v.get('parameter', [{}])[0].get('value', '')
                if isinstance(val, str) and val.startswith('AW-'):
                    ads_ids.add(val)
            print(f"Ads IDs found: {ads_ids}")
            
            # Tags
            tags = cv.get('tag', [])
            print(f"Total Tags: {len(tags)}")
            
            # List tag types
            tag_types = {}
            for t in tags:
                tt = t.get('type')
                tag_types[tt] = tag_types.get(tt, 0) + 1
            print(f"Tag Types: {tag_types}")
            
            # Check for Stape Data Tag (cvt_MBTSV is common, or custom)
            for t in tags:
                # Data Tag usually
                if t.get('name') == 'Data Tag' or 'stape' in t.get('name', '').lower():
                    print(f"Stape Data Tag Found: {t.get('name')} (Type: {t.get('type')})")
                    # Extract URL config
                    for p in t.get('parameter', []):
                        if p.get('key') == 'gtm_server_domain':
                             print(f"  Domain: {p.get('value')}")
                        if p.get('key') == 'request_path':
                             print(f"  Path: {p.get('value')}")

    except Exception as e:
        print(f"Error {label}: {e}")

def check_sgtm_clients():
    print(f"\n--- sGTM Clients ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Built-in or custom clients are in 'client' list?
            # sGTM structure might be slightly different or under 'containerVersion'
            cv = data.get('containerVersion', {})
            clients = cv.get('client', [])
            print(f"Total Clients: {len(clients)}")
            
            for c in clients:
                print(f"Client: {c.get('name')} (Type: {c.get('type')})")
                # Look for path
                for p in c.get('parameter', []):
                    # Data Client path param is often specific
                    if p.get('key') == 'pathSettings':
                        print(f"  Path Settings found")
                    if p.get('key') == 'path':
                        print(f"  Path Claim: {p.get('list')}")

    except Exception as e:
        print(f"Error Checking Clients: {e}")

if __name__ == "__main__":
    extract_from_container(web_gtm_path, "Web GTM")
    extract_from_container(sgtm_path, "sGTM")
    check_sgtm_clients()

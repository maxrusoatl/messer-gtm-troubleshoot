import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\GTM-MNRP4PF_workspace253.json"
sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\GTM-K3CQBMZ9_workspace40.json"

def inspect_details():
    print("--- sGTM Data Client Config ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            clients = data.get('containerVersion', {}).get('client', [])
            for c in clients:
                if 'Data Client' in c.get('name', ''):
                    print(f"Client: {c.get('name')}")
                    print(json.dumps(c.get('parameter', []), indent=2))
    except Exception as e:
        print(f"Error sGTM: {e}")

    print("\n--- Web GTM Google Tag Config ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            tags = data.get('containerVersion', {}).get('tag', [])
            for t in tags:
                if t.get('name') == 'Google Tag' or t.get('type') == 'googtag':
                    print(f"Tag: {t.get('name')} (Type: {t.get('type')})")
                    print(json.dumps(t.get('parameter', []), indent=2))
    except Exception as e:
        print(f"Error Web GTM: {e}")

if __name__ == "__main__":
    inspect_details()

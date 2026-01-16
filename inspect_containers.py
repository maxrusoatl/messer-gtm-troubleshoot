import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"
sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_sgtm_messerattach_com_2026_01_15.json"

def inspect_containers(path, label):
    print(f"\n--- {label} Container Inspection ---")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            containers = data.get('data', {}).get('containers', [])
            print(f"Number of containers: {len(containers)}")
            
            for i, c in enumerate(containers):
                print(f"Container {i} keys: {list(c.keys())}")
                print(f"Container {i} ID: {c.get('publicId')}")
                if 'messages' in c:
                    print(f"Container {i} messages count: {len(c['messages'])}")
                    # Print first message keys to understand structure
                    if len(c['messages']) > 0:
                        print(f"First message keys: {list(c['messages'][0].keys())}")
                        # Check for view_item in messages
                        vi_count = 0
                        for m in c['messages']:
                            if 'view_item' in json.dumps(m):
                                vi_count += 1
                        print(f"Messages containing 'view_item': {vi_count}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_containers(web_gtm_path, "Web GTM")
    inspect_containers(sgtm_path, "sGTM")

import json

path_w = r"c:\Users\maxru\max_projects\TenantAds\backend\tenantads-docker\messer-gtm-troubleshoot\original-data\tag_assistant_messerattach_com_2026_01_15.json"

def inspect_containers(path):
    print(f"--- Inspecting Containers in {path} ---")
    with open(path, 'r', encoding='utf-8') as f:
        content = json.load(f)
        containers = content.get('data', {}).get('containers', [])
        print(f"Number of containers: {len(containers)}")
        for i, c in enumerate(containers):
            print(f"Container {i} Keys: {c.keys()}")
            # Check for ID
            print(f"Container {i} ID?: {c.get('containerId')}") # Might be 'id' or nested
            if 'containerId' not in c:
                # Try to find ID elsewhere
                print(f"Sample values: {str(c)[:100]}")

inspect_containers(path_w)

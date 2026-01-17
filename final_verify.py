import json
import csv

sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_sgtm_messerattach_com_2026_01_15.json"
logs_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\stape io messer logs.csv"

def check_sgtm_exact():
    print("--- sGTM Exact Count ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Try to navigate cleanly
            # structure: data -> containers -> [0] -> messages
            c = data.get('data', {}).get('containers', [])
            if c:
                msgs = c[0].get('messages', [])
                print(f"Container 0 Messages: {len(msgs)}")
            else:
                print("No containers found in sGTM export")
    except Exception as e:
        print(f"Error sGTM: {e}")

def check_logs_403():
    print("\n--- Logs 403 Check ---")
    try:
        with open(logs_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count_403 = 0
            for row in reader:
                if row.get('Response Status Code') == '403':
                    count_403 += 1
                    print(f"403 Log: {row.get('Request Url')}")
            print(f"Total 403s in Stape Logs: {count_403}")
    except Exception as e:
        print(f"Error Logs: {e}")

if __name__ == "__main__":
    check_sgtm_exact()
    check_logs_403()

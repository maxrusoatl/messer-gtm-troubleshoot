import json
import re

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"
sgtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_sgtm_messerattach_com_2026_01_15.json"

def count_web_events():
    print("--- Web GTM Event Counts ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            c = data.get('data', {}).get('containers', [])[0]
            messages = c.get('messages', [])
            
            # Regex from trigger
            # ^(add_payment_info|add_to_cart|begin_checkout|find_location|generate_lead|login|page_view|purchase|refund|search|share|sign_up|view_cart|view_item|view_item_list|view_search_results)$
            pattern = re.compile(r"^(add_payment_info|add_to_cart|begin_checkout|find_location|generate_lead|login|page_view|purchase|refund|search|share|sign_up|view_cart|view_item|view_item_list|view_search_results)$")
            
            matching_events = 0
            page_view_count = 0
            ecom_count = 0
            
            for msg in messages:
                ename = msg.get('eventName', '')
                if ename == 'page_view':
                    page_view_count += 1
                
                if pattern.match(ename):
                    matching_events += 1
                    if ename != 'page_view':
                        ecom_count += 1
                        
            print(f"Total messages: {len(messages)}")
            print(f"Events matching regex: {matching_events}")
            print(f"  page_view count: {page_view_count}")
            print(f"  e-com count (rest): {ecom_count}")
            print(f"Data Tag Firings (from tagsFired): 12") # Hardcoded from prev finding
            
    except Exception as e:
        print(f"Error Web: {e}")

def check_sgtm_claims():
    print("\n--- sGTM Client Claims ---")
    try:
        with open(sgtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            c = data.get('data', {}).get('containers', [])[0]
            messages = c.get('messages', [])
            
            # In sGTM, messages represent requests.
            # Look for keys like 'requestUrl', 'clientName' (sometimes inferred)
            # OR 'interimEvent' -> 'client'
            
            claims = 0
            data_client_claims = 0
            
            print(f"Total sGTM messages: {len(messages)}")
            if len(messages) > 0:
                print(f"First message keys: {list(messages[0].keys())}")
            
            for msg in messages:
                # Check how client is identified
                # Maybe in 'eventData' -> 'client'?
                # Or 'trace' info?
                
                # Check for request URL to see what hit the server
                req = msg.get('request', {}) # hypothetical
                if not req:
                     # sometimes data is flat
                     pass
                
                # Let's simple check if 'Data Client' string appears in the message
                s = json.dumps(msg)
                if 'Data Client' in s:
                    data_client_claims += 1
                
                if '/data' in s:
                    print(f"Found /data in message (potential claim)")

            print(f"Messages mentioning 'Data Client': {data_client_claims}")

    except Exception as e:
        print(f"Error sGTM: {e}")

if __name__ == "__main__":
    count_web_events()
    check_sgtm_claims()

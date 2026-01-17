import json

web_gtm_path = "c:\\Users\\maxru\\max_projects\\TenantAds\\backend\\tenantads-docker\\messer-gtm-troubleshoot\\original-data\\tag_assistant_messerattach_com_2026_01_15.json"

def analyze_triggers():
    print("--- Trigger Analysis for Data Tag ---")
    try:
        with open(web_gtm_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            c = data.get('data', {}).get('containers', [])[0] # Assuming first container is Web
            
            tags_fired = c.get('tagsFired', {})
            dt_firings = tags_fired.get('Data Tag', [])
            
            print(f"Data Tag Firing Count: {len(dt_firings)}")
            for i, fire in enumerate(dt_firings):
                # Try to find the event that caused this
                # The fire object usually links back to the message index
                msg_idx = fire.get('messageIndex')
                if msg_idx is not None:
                    # Find the message
                    msgs = c.get('messages', [])
                    if msg_idx < len(msgs):
                        msg = msgs[msg_idx]
                        print(f"Firing {i}: Triggered by Event '{msg.get('eventName')}' (Index {msg_idx})")
                    else:
                        print(f"Firing {i}: Index {msg_idx} out of range")
                else:
                    print(f"Firing {i}: No message index linked")

            print("\n--- Events where Data Tag did NOT fire ---")
            messages = c.get('messages', [])
            for msg in messages:
                ename = msg.get('eventName')
                if ename in ['view_item', 'add_to_cart', 'begin_checkout', 'purchase']:
                    idx = msg.get('index')
                    # Check if Data Tag fired for this index
                    # We need to scan dt_firings to see if any have messageIndex == idx
                    fired = any(f.get('messageIndex') == idx for f in dt_firings)
                    if not fired:
                        print(f"Event '{ename}' (Index {idx}): Data Tag NOT fired")
                        # We should check WHY. 
                        # In Tag Assistant JSON, there's often 'tagEvaluation' or similar, but complex to parse.
                        # We'll rely on the previous trigger config check: Trigger 307 (ce_ecom).
                        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_triggers()

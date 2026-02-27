import json
import asyncio
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

# Configuration
API_ID = '22727397'
API_HASH = 'bfd549b603b93787f122c6efbbd76fab'
SESSION_STRING = '1BJWap1wBu7NwMuZO1b7KOB-OFIDCzlIEQcpQLyatztOdCB-BceDm61rI-XGsrzx6Zc8g_p1Gg58eqX_hlm-gB_ThpaxTd_tUIel4an2khNfT8EEGQ1C3T8l-W4AFy6TB1GMq8sSefzW5W-t6rIuUycsiUF2h49P3Roc0jmPxMK8Ktcb0MOE0caEhVvLiXfyAln9aPNzQ89LE4iGTxkCizxhDJ1bBfhZZiavEuPE0hOlTWr3_D9AppM-j8QRp1jRWovoSJUc6MxtKEzGIF-uPLGvW29EhjAHVt-m_a_Je40HF36fD62uB90cKPVsu2TkXnA_WQz5ekenctKY6sZKTxNnGW8tDp_o='

async def audit_groups():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    
    with open('discovered_groups.json', 'r') as f:
        discovered = json.load(f)

    print("Auditing groups for promotion activity...")
    active_promo_groups = []

    for group in discovered:
        try:
            print(f"Auditing: {group['title']}...")
            entity = await client.get_entity(group['username'])
            
            # Get last 20 messages to see if there's high promo activity
            messages = await client.get_messages(entity, limit=20)
            
            promo_count = 0
            for msg in messages:
                if msg.text:
                    text = msg.text.lower()
                    # Keywords that signal a reselling/promo environment
                    if any(k in text for k in ['wts', 'wtb', 'available', 'price', '$', 'dm', 'escrow', 'verified', 'service']):
                        promo_count += 1
            
            # If more than 30% of recent messages look like promos, it's a "Green" group
            if promo_count >= 6:
                print(f"✅ HIGH PROMO ACTIVITY: {group['title']}")
                active_promo_groups.append(group)
            else:
                print(f"❌ Low/No promo activity: {group['title']}")
                
        except Exception as e:
            print(f"Could not audit {group['username']}: {e}")

    with open('vetted_promo_groups.json', 'w') as f:
        json.dump(active_promo_groups, f, indent=2)
    
    print(f"\nAudit Complete. Found {len(active_promo_groups)} vetted promo groups.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(audit_groups())

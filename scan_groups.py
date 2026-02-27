import json
import asyncio
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

# Config
with open('userbot_config.json', 'r') as f:
    config = json.load(f)

SESSION_STRING = '1BJWap1wBu7NwMuZO1b7KOB-OFIDCzlIEQcpQLyatztOdCB-BceDm61rI-XGsrzx6Zc8g_p1Gg58eqX_hlm-gB_ThpaxTd_tUIel4an2khNfT8EEGQ1C3T8l-W4AFy6TB1GMq8sSefzW5W-t6rIuUycsiUF2h49P3Roc0jmPxMK8Ktcb0MOE0caEhVvLiXfyAln9aPNzQ89LE4iGTxkCizxhDJ1bBfhZZiavEuPE0hOlTWr3_D9AppM-j8QRp1jRWovoSJUc6MxtKEzGIF-uPLGvW29EhjAHVt-m_a_Je40HF36fD62uB90cKPVsu2TkXnA_WQz5ekenctKY6sZKTxNnGW8tDp_o='

# Keywords to find relevant groups
KEYWORDS = ['resell', 'otc', 'llc', 'account', 'relay', 'mercury', 'airwallex', 'selling', 'buy', 'business', 'p2p', 'escrow', 'service']

async def scan_groups():
    client = TelegramClient(StringSession(SESSION_STRING), config['api_id'], config['api_hash'])
    await client.connect()
    
    print("Scanning your groups and channels...")
    relevant_groups = []
    all_dialogs = await client.get_dialogs()
    
    for dialog in all_dialogs:
        if dialog.is_group or dialog.is_channel:
            name = dialog.name.lower()
            # Check if name contains keywords
            is_relevant = any(keyword in name for keyword in KEYWORDS)
            
            if is_relevant:
                # Try to get username if it exists
                username = dialog.entity.username if hasattr(dialog.entity, 'username') and dialog.entity.username else str(dialog.id)
                relevant_groups.append({
                    "name": dialog.name,
                    "id": str(dialog.id),
                    "username": username
                })
                print(f"FOUND RELEVANT: {dialog.name}")

    # Save found groups to a new config file
    with open('relevant_groups.json', 'w') as f:
        json.dump(relevant_groups, f, indent=2)
    
    print(f"\nScan complete. Found {len(relevant_groups)} relevant groups.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(scan_groups())

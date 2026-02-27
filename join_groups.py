import json
import asyncio
import random
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

# Configuration
API_ID = '22727397'
API_HASH = 'bfd549b603b93787f122c6efbbd76fab'
SESSION_STRING = '1BJWap1wBu7NwMuZO1b7KOB-OFIDCzlIEQcpQLyatztOdCB-BceDm61rI-XGsrzx6Zc8g_p1Gg58eqX_hlm-gB_ThpaxTd_tUIel4an2khNfT8EEGQ1C3T8l-W4AFy6TB1GMq8sSefzW5W-t6rIuUycsiUF2h49P3Roc0jmPxMK8Ktcb0MOE0caEhVvLiXfyAln9aPNzQ89LE4iGTxkCizxhDJ1bBfhZZiavEuPE0hOlTWr3_D9AppM-j8QRp1jRWovoSJUc6MxtKEzGIF-uPLGvW29EhjAHVt-m_a_Je40HF36fD62uB90cKPVsu2TkXnA_WQz5ekenctKY6sZKTxNnGW8tDp_o='

async def join_discovered():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    
    with open('discovered_groups.json', 'r') as f:
        discovered = json.load(f)

    print(f"Starting to join {len(discovered)} discovered groups...")
    joined_count = 0

    for group in discovered:
        # Quality filter: Skip groups with very few participants unless highly specific username
        if group['participants_count'] < 5 and len(group['username']) > 15:
            continue
            
        try:
            print(f"Joining: {group['title']} (@{group['username']})")
            await client(functions.channels.JoinChannelRequest(
                channel=group['username']
            ))
            joined_count += 1
            # Random delay to stay under the radar (15-45 seconds per join)
            wait = random.randint(15, 45)
            print(f"Successfully joined. Waiting {wait}s...")
            await asyncio.sleep(wait)
            
            # Stop after a batch to avoid aggressive behavior
            if joined_count >= 20:
                print("Batch limit reached for this run to prevent account restriction.")
                break
                
        except Exception as e:
            print(f"Failed to join {group['username']}: {e}")
            await asyncio.sleep(5)

    print(f"Finished. Total newly joined in this run: {joined_count}")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(join_discovered())

import json
import asyncio
import time
from telethon import TelegramClient, events

from telethon.sessions import StringSession

# Load config
def load_config():
    with open('userbot_config.json', 'r') as f:
        return json.load(f)

config = load_config()
SESSION_STRING = '1BJWap1wBu7NwMuZO1b7KOB-OFIDCzlIEQcpQLyatztOdCB-BceDm61rI-XGsrzx6Zc8g_p1Gg58eqX_hlm-gB_ThpaxTd_tUIel4an2khNfT8EEGQ1C3T8l-W4AFy6TB1GMq8sSefzW5W-t6rIuUycsiUF2h49P3Roc0jmPxMK8Ktcb0MOE0caEhVvLiXfyAln9aPNzQ89LE4iGTxkCizxhDJ1bBfhZZiavEuPE0hOlTWr3_D9AppM-j8QRp1jRWovoSJUc6MxtKEzGIF-uPLGvW29EhjAHVt-m_a_Je40HF36fD62uB90cKPVsu2TkXnA_WQz5ekenctKY6sZKTxNnGW8tDp_o='

client = TelegramClient(StringSession(SESSION_STRING), config['api_id'], config['api_hash'])

async def send_updates():
    while True:
        current_config = load_config()
        groups = current_config['groups']
        message = current_config['message']
        
        print(f"Starting broadcast to {len(groups)} groups...")
        
        for group in groups:
            try:
                # Resolve group/username
                entity = await client.get_entity(group)
                await client.send_message(entity, message)
                print(f"Sent to {group}")
                # Small delay to avoid flood
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Failed to send to {group}: {e}")
        
        print(f"Broadcast complete. Sleeping for {current_config['interval_seconds']} seconds.")
        await asyncio.sleep(current_config['interval_seconds'])

async def main():
    await client.start()
    print("Userbot started and authenticated.")
    await send_updates()

if __name__ == '__main__':
    client.loop.run_until_complete(main())

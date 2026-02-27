import json
import asyncio
import random
import time
import sys
from telethon import TelegramClient, errors
from telethon.sessions import StringSession

# Configuration
API_ID = '22727397'
API_HASH = 'bfd549b603b93787f122c6efbbd76fab'
SESSION_STRING = '1BJWap1wBu7NwMuZO1b7KOB-OFIDCzlIEQcpQLyatztOdCB-BceDm61rI-XGsrzx6Zc8g_p1Gg58eqX_hlm-gB_ThpaxTd_tUIel4an2khNfT8EEGQ1C3T8l-W4AFy6TB1GMq8sSefzW5W-t6rIuUycsiUF2h49P3Roc0jmPxMK8Ktcb0MOE0caEhVvLiXfyAln9aPNzQ89LE4iGTxkCizxhDJ1bBfhZZiavEuPE0hOlTWr3_D9AppM-j8QRp1jRWovoSJUc6MxtKEzGIF-uPLGvW29EhjAHVt-m_a_Je40HF36fD62uB90cKPVsu2TkXnA_WQz5ekenctKY6sZKTxNnGW8tDp_o='

BANK_PROMO = """🚀 *EXCLUSIVE BUSINESS ASSETS* 🚀
💎 **RELAY + MERCURY + AIRWALLEX** ($1800)
💎 **RELAY + MERCURY PAIR** ($1300)
💎 **RELAY + AIRWALLEX PAIR** ($1300)
✅ **RELAY LLC** ($650) | **MERCURY LLC** ($500)
✅ **AIRWALLEX LLC** ($500)
🤝 **DM FOR DEAL:** @ECAMZEBAY
🛡️ **ESCROW ALWAYS WELCOME** ++"""

ECOM_PROMO = """⚡ *PREMIUM E-COMMERCE ASSETS* ⚡
📦 **AMAZON BIZ (LLC BASED)**
↳ 2Y Old | USA ID | VC Verified | Payoneer
📦 **FRESH AMAZON USA (LLC)** + Payoneer
📦 **TIKTOK SHOP (LLC BASED)**
↳ Verified | USA ID | All Docs
🛠️ **Full Future Support Provided**
🤝 **DM FOR DEAL:** @ECAMZEBAY
🛡️ **ESCROW WELCOME** ++"""

# Short version for restricted groups (<400 chars)
ECOM_SHORT = """⚡ *AMAZON & TIKTOK ASSETS* ⚡
📦 **AMAZON LLC BIZ** (2Y Old, VC Verified)
📦 **FRESH AMAZON USA LLC**
📦 **TIKTOK SHOP LLC** (Verified)
↳ Includes Payoneer & Future Support.
🤝 **DM:** @ECAMZEBAY | 🛡️ ESCROW ++"""

LOG_FILE = 'bot_activity.json'

def log_activity(group_name, promo_type):
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = []
    data.append({"group": group_name, "type": promo_type, "timestamp": time.time()})
    with open(LOG_FILE, 'w') as f:
        json.dump(data[-500:], f, indent=2)

async def run_automation():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    me = await client.get_me()
    print(f"Logged in as {me.first_name}. FAST MODE + LENGTH CHECK ACTIVE.")

    while True:
        try:
            with open('bank_otc_groups.json', 'r') as f:
                bank_groups = json.load(f)
            with open('ecommerce_groups.json', 'r') as f:
                ecom_groups = json.load(f)

            tasks = []
            for g in bank_groups:
                tasks.append((g, BANK_PROMO, 'BANK'))
            for g in ecom_groups:
                # Special check for known restricted group
                if g['username'] == 'AmazonSellerSupportService':
                    tasks.append((g, ECOM_SHORT, 'ECOM'))
                else:
                    tasks.append((g, ECOM_PROMO, 'ECOM'))

            random.shuffle(tasks)

            for g_info, message, p_type in tasks:
                target = g_info['username'] if g_info['username'] else int(g_info['id'])
                try:
                    entity = await client.get_entity(target)
                    print(f"FAST SENDING -> {g_info['name']} (Length: {len(message)})")
                    await client.send_message(entity, message)
                    log_activity(g_info['name'], p_type)
                    await asyncio.sleep(random.randint(3, 7))
                except errors.FloodWaitError as e:
                    print(f"FLOOD WAIT: {e.seconds}s")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    print(f"ERROR {g_info['name']}: {e}")
                    await asyncio.sleep(2)

            print("Cycle complete. Waiting 1 hour...")
            await asyncio.sleep(3600)
            
        except Exception as e:
            print(f"GLOBAL ERROR: {e}")
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(run_automation())

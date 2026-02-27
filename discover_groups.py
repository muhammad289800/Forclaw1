import json
import asyncio
import random
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession

# Configuration
API_ID = '22727397'
API_HASH = 'bfd549b603b93787f122c6efbbd76fab'
SESSION_STRING = '1BJWap1wBu7NwMuZO1b7KOB-OFIDCzlIEQcpQLyatztOdCB-BceDm61rI-XGsrzx6Zc8g_p1Gg58eqX_hlm-gB_ThpaxTd_tUIel4an2khNfT8EEGQ1C3T8l-W4AFy6TB1GMq8sSefzW5W-t6rIuUycsiUF2h49P3Roc0jmPxMK8Ktcb0MOE0caEhVvLiXfyAln9aPNzQ89LE4iGTxkCizxhDJ1bBfhZZiavEuPE0hOlTWr3_D9AppM-j8QRp1jRWovoSJUc6MxtKEzGIF-uPLGvW29EhjAHVt-m_a_Je40HF36fD62uB90cKPVsu2TkXnA_WQz5ekenctKY6sZKTxNnGW8tDp_o='

# Search Keywords for high-value groups
SEARCH_QUERIES = [
    'Amazon Seller', 'Amazon FBA Business', 'eBay Seller Group', 'Walmart Marketplace',
    'Shopify Dropshipping', 'TikTok Shop Sellers', 'Digital Assets OTC', 'Bank Account LLC',
    'Escrow Service', 'Business flipping', 'Payoneer Verified', 'Stripe verified',
    'Wise Business', 'Mercury Bank', 'Relay Bank'
]

async def discover_and_join():
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.connect()
    
    new_groups = []
    print(f"Starting discovery for {len(SEARCH_QUERIES)} niches...")

    for query in SEARCH_QUERIES:
        print(f"Searching for: {query}")
        result = await client(functions.contacts.SearchRequest(
            q=query,
            limit=10
        ))
        
        for chat in result.chats:
            # Filter for groups/channels that are public and have usernames
            if hasattr(chat, 'username') and chat.username:
                # Basic filter to avoid joining junk (can be refined)
                if not chat.left: # Already a member?
                    continue
                
                new_groups.append({
                    "title": chat.title,
                    "username": chat.username,
                    "id": chat.id,
                    "participants_count": getattr(chat, 'participants_count', 0)
                })

    # Save discovery results
    with open('discovered_groups.json', 'w') as f:
        json.dump(new_groups, f, indent=2)
    
    print(f"Discovery complete. Found {len(new_groups)} potential groups.")
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(discover_and_join())

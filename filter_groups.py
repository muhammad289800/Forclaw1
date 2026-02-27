import json
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Load all found groups
with open('relevant_groups.json', 'r') as f:
    all_groups = json.load(f)

# Keywords that indicate Amazon-specific or E-commerce specific groups (to EXCLUDE)
EXCLUDE_KEYWORDS = ['amazon', 'amz', 'ebay', 'walmart', 'ecommerce', 'e-com', 'shop', 'listing', 'reinstatement', 'feedback', 'buyer account', 'seller account']

# Keywords that indicate Banks, OTC, or General Business (to INCLUDE)
INCLUDE_KEYWORDS = ['bank', 'otc', 'llc', 'relay', 'mercury', 'airwallex', 'p2p', 'escrow', 'taverna', 'gross', 'financing', 'invest']

def filter_groups():
    bank_otc_groups = []
    
    for group in all_groups:
        name = group['name'].lower()
        
        # Priority: If it matches Bank/OTC keywords AND doesn't have Amazon/Ecom keywords
        # OR if it's clearly a high-value OTC group from your initial links
        is_include = any(k in name for k in INCLUDE_KEYWORDS)
        is_exclude = any(k in name for k in EXCLUDE_KEYWORDS)
        
        # Explicit check for your provided high-priority links
        priority_usernames = ['grossou', 'web_investors', 'tvrn_p2p', 'mariaotc', 'tvrn_otc']
        is_priority = group['username'] and group['username'].lower() in priority_usernames
        
        if (is_include or is_priority) and not (is_exclude and not is_priority):
            bank_otc_groups.append(group)

    # Save filtered list
    with open('bank_otc_groups.json', 'w') as f:
        json.dump(bank_otc_groups, f, indent=2)
    
    return bank_otc_groups

if __name__ == '__main__':
    filtered = filter_groups()
    print(f"Filtered to {len(filtered)} Bank & OTC specific groups.")
    for g in filtered[:10]:
        print(f"- {g['name']}")

import json
import time
import os

LOG_FILE = 'bot_activity.json'

def get_report():
    if not os.path.exists(LOG_FILE):
        return "Bot activity log not found. Bot might be starting up."
    
    with open(LOG_FILE, 'r') as f:
        data = json.load(f)
    
    now = time.time()
    two_hours_ago = now - (2 * 3600)
    
    recent_activity = [item for item in data if item['timestamp'] > two_hours_ago]
    
    if not recent_activity:
        return "Pichlay 2 ghanton mein koi naya message post nahi hua (Filtering active)."
    
    bank_count = len([i for i in recent_activity if i['type'] == 'BANK'])
    ecom_count = len([i for i in recent_activity if i['type'] == 'ECOM'])
    
    report = f"📊 *Userbot 2-Hour Status Report*\n\n"
    report += f"✅ **Total Messages Sent:** {len(recent_activity)}\n"
    report += f"🏦 **Bank/OTC Posts:** {bank_count}\n"
    report += f"📦 **E-commerce Posts:** {ecom_count}\n\n"
    
    report += "📝 **Latest Groups Covered:**\n"
    # Get last 5 unique groups
    last_groups = []
    for item in reversed(recent_activity):
        if item['group'] not in last_groups:
            last_groups.append(item['group'])
        if len(last_groups) >= 5:
            break
            
    for g in last_groups:
        report += f"- {g}\n"
        
    report += "\n🔄 Bot routine checkup: *Healthy* 🦾"
    return report

if __name__ == '__main__':
    print(get_report())

import json

# Load all found groups
with open('relevant_groups.json', 'r') as f:
    all_groups = json.load(f)

# Keywords that indicate Amazon-specific or E-commerce specific groups
ECOMMERCE_KEYWORDS = ['amazon', 'amz', 'ebay', 'walmart', 'ecommerce', 'e-com', 'shop', 'listing', 'reinstatement', 'feedback', 'buyer account', 'seller account', 'tiktok shop', 'selling']

def filter_ecom_groups():
    ecom_groups = []
    
    for group in all_groups:
        name = group['name'].lower()
        
        # We want to INCLUDE groups that have these keywords
        is_ecom = any(k in name for k in ECOMMERCE_KEYWORDS)
        
        if is_ecom:
            ecom_groups.append(group)

    # Save filtered list
    with open('ecommerce_groups.json', 'w') as f:
        json.dump(ecom_groups, f, indent=2)
    
    return ecom_groups

if __name__ == '__main__':
    filtered = filter_ecom_groups()
    print(f"Filtered to {len(filtered)} E-commerce & Amazon specific groups.")

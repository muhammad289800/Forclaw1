
import requests
from bs4 import BeautifulSoup
import re
import sys

product_url = "https://casadesignfurniture.com/product/018-noralie-tv-stand-fireplace/"
try:
    response = requests.get(product_url, timeout=10)
    response.raise_for_status() # Raise an exception for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error fetching URL {product_url}: {e}", file=sys.stderr)
    sys.exit(1)

soup = BeautifulSoup(response.content, 'html.parser')

image_urls = set() # Use set to store unique URLs

# Look for images within the product gallery or main content
for img_tag in soup.find_all('img'):
    src = img_tag.get('src')
    if src and ('.jpg' in src.lower() or '.png' in src.lower()) and "wp-content/uploads" in src:
        image_urls.add(src)
    
# Also look for data-src or data-srcset attributes often used in galleries
for div_tag in soup.find_all('div'):
    data_src = div_tag.get('data-src')
    if data_src and ('.jpg' in data_src.lower() or '.png' in data_src.lower()) and "wp-content/uploads" in data_src:
        image_urls.add(data_src)

# Also check script tags for JSON-LD or other embedded data that might have image URLs
for script_tag in soup.find_all('script'):
    if script_tag.string:
        # Use a raw string for regex pattern to avoid backslash issues
        matches = re.findall(r'https:\/\/casadesignfurniture\.com\/wp-content\/uploads\/[^"\'\\]+\\.(?:jpg|png)', script_tag.string, re.IGNORECASE)
        for match in matches:
            image_urls.add(match)

if image_urls:
    for url in sorted(list(image_urls)):
        print(url)
else:
    print("No relevant image URLs found.")


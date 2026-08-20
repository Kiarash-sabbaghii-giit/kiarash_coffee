import requests
from bs4 import BeautifulSoup
import time
import re
from config import Config
from connection import connect_to_mongodb


def clean_price(price_text):
    """Clean price from commas and extra characters"""
    if not price_text:
        return ""
    return re.sub(r'[^\d]', '', price_text)


def extract_product_info(product_element):
    """Extract product information from element"""
    try:
        persian_name = ""
        english_name = ""
        description = ""
        price = ""
        price_type = ""

        # Get all text lines
        all_text = product_element.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]

        # Remove duplicates
        unique_lines = []
        seen = set()
        for line in lines:
            if line not in seen and len(line) > 1:
                seen.add(line)
                unique_lines.append(line)
        lines = unique_lines

        # Find Persian name
        for line in lines:
            if re.search(r'[آ-ی]', line) and len(line) > 2:
                if not re.search(r'\d', line) and not any(k in line for k in ['تک', 'جفت', 'کوچک', 'متوسط', 'بزرگ']):
                    if not persian_name:
                        persian_name = line
                        break

        # Find English name
        for line in lines:
            if re.search(r'[A-Za-z]', line) and len(line) > 2:
                if not re.search(r'[آ-ی]', line):
                    english_name = line
                    break

        # Find price type
        price_keywords = ['تک شات', 'جفت شات', 'کوچک', 'متوسط', 'بزرگ']
        for line in lines:
            if any(keyword in line for keyword in price_keywords):
                price_type = line
                break

        # Find price
        for line in lines:
            if re.search(r'\d{1,3}(?:,\d{3})*', line):
                price = clean_price(line)
                break

        # Find description
        for line in lines:
            if 'محتویات' in line or 'مواد' in line or ':' in line:
                description = line
                break

        # Get image URL
        img_tag = product_element.find('img')
        img_url = ""
        if img_tag:
            img_url = img_tag.get('src', '')
            if not img_url:
                img_url = img_tag.get('data-src', '')

        return {
            'persian_name': persian_name,
            'english_name': english_name,
            'price': price,
            'price_type': price_type,
            'image_url': img_url,
            'description': description
        }

    except Exception as e:
        print(f"Error extracting product info: {e}")
        return None


def scrape_all_menus():
    """Scrape all menus"""
    db = connect_to_mongodb()
    if db is None:
        return

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        print(f"🔍 Fetching menu from {Config.MENU_URL}...")
        response = requests.get(Config.MENU_URL, headers=headers, timeout=Config.REQUEST_TIMEOUT)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"❌ Failed to fetch page: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        tabs = soup.find_all('span', class_='jet-tabs__label-text')
        contents = soup.find_all('div', class_='jet-tabs__content')

        print(f"\n✅ Found {len(tabs)} menu tabs")
        print("=" * 60)

        total_added = 0

        for i, tab in enumerate(tabs):
            menu_name = tab.text.strip()

            if menu_name in Config.MENU_MAPPING:
                collection_name = Config.MENU_MAPPING[menu_name]
                print(f"\n📋 Scraping {menu_name} -> {collection_name}")

                content_div = None
                parent_tab = tab.find_parent('div', class_='jet-tabs__control')
                if parent_tab:
                    tab_id = parent_tab.get('id', '')
                    if tab_id:
                        content_div = soup.find('div', {'aria-labelledby': tab_id})

                if not content_div and i < len(contents):
                    content_div = contents[i]

                if content_div:
                    product_items = content_div.find_all('div', class_='jet-listing-grid__item')

                    if not product_items:
                        product_items = content_div.find_all('div', class_='elementor-widget-container')

                    print(f"  🔍 Found {len(product_items)} products")

                    if product_items:
                        collection = db[collection_name]
                        added_count = 0

                        for product_element in product_items:
                            product_info = extract_product_info(product_element)

                            if product_info and product_info['persian_name']:
                                unique_key = {
                                    'persian_name': product_info['persian_name'],
                                    'price_type': product_info['price_type'] if product_info['price_type'] else ""
                                }

                                existing = collection.find_one(unique_key)
                                if not existing:
                                    collection.insert_one(product_info)
                                    added_count += 1
                                    total_added += 1
                                    type_info = f" ({product_info['price_type']})" if product_info['price_type'] else ""
                                    price_display = f" - {product_info['price']} تومان" if product_info['price'] else ""
                                    print(f"  ✅ {product_info['persian_name']}{type_info}{price_display}")

                        print(f"  📊 Added {added_count} products to {collection_name}")

                time.sleep(Config.REQUEST_DELAY)

        print("\n" + "=" * 60)
        print(f"✅ Scraping complete! Total {total_added} new products added.")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Error during scraping: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 Lamiz Coffee Menu Scraper")
    print("=" * 60)
    scrape_all_menus()
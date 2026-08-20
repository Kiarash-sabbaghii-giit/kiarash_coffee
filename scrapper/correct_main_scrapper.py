import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
from config import Config
from connection import connect_to_mongodb


def clean_price(price_text):
    """Clean price from commas and extra characters"""
    if not price_text:
        return ""
    return re.sub(r'[^\d]', '', price_text)


def extract_all_variants_from_element(product_element):
    """Extract all price variants from a product element"""
    try:
        variants = []

        # Get all text
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
        persian_name = ""
        for line in lines:
            if re.search(r'[آ-ی]', line) and len(line) > 2:
                if not re.search(r'\d', line) and not any(k in line for k in ['تک', 'جفت', 'کوچک', 'متوسط', 'بزرگ']):
                    if not persian_name:
                        persian_name = line
                        break

        # Find English name
        english_name = ""
        for line in lines:
            if re.search(r'[A-Za-z]', line) and len(line) > 2:
                if not re.search(r'[آ-ی]', line):
                    english_name = line
                    break

        # Find description
        description = ""
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
            if img_url and not img_url.startswith('http'):
                img_url = urljoin('https://lamizcoffee.com/', img_url)

        # Price type keywords
        type_keywords = ['تک شات', 'جفت شات', 'کوچک', 'متوسط', 'بزرگ']

        # Find type lines
        type_lines = []
        for i, line in enumerate(lines):
            for keyword in type_keywords:
                if keyword in line:
                    type_lines.append((i, line, keyword))
                    break

        if type_lines:
            for idx, type_line, keyword in type_lines:
                price = ""
                for j in range(idx + 1, len(lines)):
                    if re.search(r'\d{1,3}(?:,\d{3})*', lines[j]):
                        price = clean_price(lines[j])
                        break

                variants.append({
                    'persian_name': persian_name,
                    'english_name': english_name,
                    'price': price,
                    'price_type': keyword,
                    'image_url': img_url,
                    'description': description
                })
        else:
            # Find all prices
            prices = []
            for line in lines:
                if re.search(r'\d{1,3}(?:,\d{3})*', line):
                    price = clean_price(line)
                    if not any(k in line for k in type_keywords):
                        prices.append(price)

            if len(prices) > 1:
                for i, price in enumerate(prices, 1):
                    variants.append({
                        'persian_name': persian_name,
                        'english_name': english_name,
                        'price': price,
                        'price_type': f"نوع {i}",
                        'image_url': img_url,
                        'description': description
                    })
            elif len(prices) == 1:
                variants.append({
                    'persian_name': persian_name,
                    'english_name': english_name,
                    'price': prices[0],
                    'price_type': "",
                    'image_url': img_url,
                    'description': description
                })
            else:
                variants.append({
                    'persian_name': persian_name,
                    'english_name': english_name,
                    'price': "",
                    'price_type': "",
                    'image_url': img_url,
                    'description': description
                })

        return variants

    except Exception as e:
        print(f"Error extracting variants: {e}")
        return []


def scrape_all_menus_with_variants():
    """Scrape all menus with price variant support"""
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

                    if not product_items:
                        product_items = content_div.find_all('div', recursive=True)
                        filtered = []
                        for item in product_items:
                            if item.find('img') and len(item.get_text(strip=True)) > 20:
                                filtered.append(item)
                        product_items = filtered

                    print(f"  🔍 Found {len(product_items)} products")

                    if product_items:
                        collection = db[collection_name]
                        added_count = 0

                        for product_element in product_items:
                            variants = extract_all_variants_from_element(product_element)

                            for variant in variants:
                                if variant and variant['persian_name']:
                                    unique_key = {
                                        'persian_name': variant['persian_name'],
                                        'price_type': variant['price_type'] if variant['price_type'] else ""
                                    }

                                    existing = collection.find_one(unique_key)
                                    if not existing:
                                        collection.insert_one(variant)
                                        added_count += 1
                                        total_added += 1
                                        type_info = f" ({variant['price_type']})" if variant['price_type'] else ""
                                        price_display = f" - {variant['price']} تومان" if variant['price'] else ""
                                        print(f"  ✅ {variant['persian_name']}{type_info}{price_display}")

                        print(f"  📊 Added {added_count} products to {collection_name}")

                time.sleep(Config.REQUEST_DELAY)

        print("\n" + "=" * 60)
        print(f"✅ Scraping complete! Total {total_added} new products added.")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Error during scraping: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 Lamiz Coffee Menu Scraper (Multi-Price Support)")
    print("=" * 60)
    scrape_all_menus_with_variants()
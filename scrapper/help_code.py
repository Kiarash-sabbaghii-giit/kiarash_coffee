import requests
from bs4 import BeautifulSoup
import re
from config import Config
from connection import connect_to_mongodb


def extract_product_info(product_element):
    """Extract product information"""
    try:
        all_text = product_element.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]

        persian_name = ""
        english_name = ""
        description = ""
        price = ""

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

        # Find price
        for line in lines:
            if re.search(r'\d{1,3}(?:,\d{3})*', line):
                price = re.sub(r'[^\d]', '', line)
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

        return {
            'persian_name': persian_name,
            'english_name': english_name,
            'price': price,
            'image_url': img_url,
            'description': description
        }

    except Exception as e:
        return None


def scrape_cakes_and_testbar():
    """Scrape cakes and testbar specifically"""
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

        target_tabs = ['کیک‌ها', 'تست‌بار']
        target_indices = []

        for i, tab in enumerate(tabs):
            tab_name = tab.text.strip()
            if tab_name in target_tabs:
                target_indices.append(i)
                print(f"\n🎯 Found tab: {tab_name} (Index: {i})")

        if not target_indices:
            print("❌ Cakes and testbar tabs not found!")
            return

        contents = soup.find_all('div', class_='jet-tabs__content')

        for index in target_indices:
            tab = tabs[index]
            menu_name = tab.text.strip()
            collection_name = 'cakes' if menu_name == 'کیک‌ها' else 'testbar'

            print(f"\n📋 Scraping {menu_name} -> {collection_name}")

            content_div = None
            if index < len(contents):
                content_div = contents[index]

            if content_div:
                product_items = content_div.find_all('div', class_='jet-listing-grid__item')

                if not product_items:
                    product_items = content_div.find_all('div', class_='elementor-widget-container')

                print(f"  🔍 Found {len(product_items)} products")

                if product_items:
                    collection = db[collection_name]
                    count = 0

                    for product_element in product_items:
                        product_info = extract_product_info(product_element)

                        if product_info and product_info['persian_name']:
                            existing = collection.find_one({'persian_name': product_info['persian_name']})
                            if not existing:
                                collection.insert_one(product_info)
                                count += 1
                                print(f"  ✅ {product_info['persian_name']}")

                    print(f"  📊 Added {count} products to {collection_name}")

        print("\n✅ Cakes and testbar scraping complete!")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 Cakes and Testbar Scraper")
    print("=" * 60)
    scrape_cakes_and_testbar()
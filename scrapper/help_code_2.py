from config import Config
from connection import connect_to_mongodb


def format_price(price):
    """Add comma to price (e.g., 123670 -> 123,670)"""
    if not price:
        return ""
    if ',' in str(price):
        return price
    price_str = str(price).replace(',', '')
    if not price_str.isdigit():
        return price
    return f"{int(price_str):,}"


def update_all_prices():
    """Update all prices with comma formatting"""
    db = connect_to_mongodb()
    if db is None:
        return

    collections = list(Config.MENU_MAPPING.values())
    total_updated = 0

    for collection_name in collections:
        try:
            collection = db[collection_name]
            documents = collection.find({'price': {'$ne': ''}})

            updated_count = 0
            for doc in documents:
                old_price = doc.get('price', '')
                new_price = format_price(old_price)

                if old_price != new_price:
                    collection.update_one(
                        {'_id': doc['_id']},
                        {'$set': {'price': new_price}}
                    )
                    updated_count += 1
                    print(f"  🔄 {doc.get('persian_name', 'N/A')}: {old_price} -> {new_price}")

            if updated_count > 0:
                print(f"✅ {collection_name}: {updated_count} prices updated")
                total_updated += updated_count
            else:
                print(f"ℹ️ {collection_name}: No prices needed updating")

        except Exception as e:
            print(f"❌ Error in {collection_name}: {e}")

    print("\n" + "=" * 60)
    print(f"📊 Total prices updated: {total_updated}")
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 Price Formatter (Adding Commas)")
    print("=" * 60)
    update_all_prices()
    print("\n✅ Operation complete!")
    print("=" * 60)
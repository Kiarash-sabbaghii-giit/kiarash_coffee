# apps/menu/models.py

from django.db import models
from kiarash_cafe.settings import get_mongodb_connection


class Category:
    """مدل دسته‌بندی (از MongoDB)"""

    @staticmethod
    def get_all_categories():
        try:
            db = get_mongodb_connection()
            if db is None:
                return []

            categories = db['categories'].find({})
            return list(categories)
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []


class Product:
    """مدل محصول (از MongoDB)"""

    @staticmethod
    def get_products_by_category(category_name):
        """دریافت محصولات یک دسته‌بندی از MongoDB"""
        try:
            db = get_mongodb_connection()
            if db is None:
                return []

            # ===== اصلاح اینجا: استفاده از نام کلکشن به همان شکلی که هست =====
            products = db[category_name].find({})

            product_list = []
            for product in products:
                product_dict = dict(product)
                product_dict['_id'] = str(product_dict['_id'])

                # اگر محصول دارای price_type است، آن را به عنوان variant در نظر بگیر
                if product_dict.get('price_type'):
                    product_dict['variants'] = [{
                        'price_type': product_dict.get('price_type', ''),
                        'price': product_dict.get('price', '')
                    }]
                else:
                    product_dict['variants'] = []

                product_list.append(product_dict)

            return product_list
        except Exception as e:
            print(f"Error getting products from {category_name}: {e}")
            return []
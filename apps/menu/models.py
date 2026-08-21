# apps/menu/models.py

from django.db import models
from kiarash_cafe.settings import get_mongodb_connection


class Category:
    """مدل دسته‌بندی (از MongoDB)"""

    @staticmethod
    def get_all_categories():
        """دریافت تمام دسته‌بندی‌ها از MongoDB"""
        try:
            db = get_mongodb_connection()
            if db is None:
                return []

            # دریافت دسته‌بندی‌ها از یک collection خاص در MongoDB
            # اگر collection خاصی برای دسته‌بندی ندارید، از لیست ثابت استفاده کنید
            categories = db['categories'].find({})
            return list(categories)
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    @staticmethod
    def get_category_by_name(category_name):
        """دریافت یک دسته‌بندی با نام"""
        try:
            db = get_mongodb_connection()
            if db is None:
                return None

            category = db['categories'].find_one({'name': category_name})
            return category
        except Exception as e:
            print(f"Error getting category: {e}")
            return None


class Product:
    """مدل محصول (از MongoDB)"""

    @staticmethod
    def get_products_by_category(category_name):
        """دریافت محصولات یک دسته‌بندی از MongoDB"""
        try:
            db = get_mongodb_connection()
            if db is None:
                return []

            # دریافت محصولات از کلکشن مربوطه
            collection_name = category_name.lower().replace(' ', '_')
            products = db[collection_name].find({})

            # تبدیل به لیست و اضافه کردن variants
            product_list = []
            for product in products:
                # ایجاد لیست variants برای هر محصول
                product_dict = dict(product)
                product_dict['_id'] = str(product_dict['_id'])  # تبدیل ObjectId به string

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
            print(f"Error getting products: {e}")
            return []

    @staticmethod
    def get_all_products():
        """دریافت تمام محصولات از MongoDB"""
        try:
            db = get_mongodb_connection()
            if db is None:
                return []

            all_products = []
            # لیست کلکشن‌های محصولات
            collections = [
                'hot_drinks', 'cold_drinks', 'Seasonal_Promotion',
                'matcha', 'healthy_menu', 'Brewed_coffee', 'tea',
                'elcless', 'cakes', 'testbar', 'crosan_sandwich', 'popsickle'
            ]

            for collection_name in collections:
                products = db[collection_name].find({})
                for product in products:
                    product_dict = dict(product)
                    product_dict['_id'] = str(product_dict['_id'])
                    product_dict['category'] = collection_name
                    all_products.append(product_dict)

            return all_products
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for loading environment variables"""

    # MongoDB Settings
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
    MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'kiarash_cafe')

    # Website Settings
    WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://lamizcoffee.com/')
    MENU_URL = os.getenv('MENU_URL', 'https://lamizcoffee.com/lamiz-coffee-menu/')

    # Scraping Settings
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    REQUEST_DELAY = float(os.getenv('REQUEST_DELAY', 0.5))

    # Menu mapping (Persian to English collection names)
    MENU_MAPPING = {
        'نوشیدنی گرم': 'hot_drinks',
        'نوشیدنی سرد': 'cold_drinks',
        'پروموشن فصلی': 'Seasonal_Promotion',
        'ماچا': 'matcha',
        'منو سلامت': 'healthy_menu',
        'قهوه دمی': 'Brewed_coffee',
        'چای و دمنوش': 'tea',
        'منو خاموشی': 'elcless',
        'کیک‌ها': 'cakes',
        'تست‌بار': 'testbar',
        'ساندویچ کراسان': 'crosan_sandwich',
        'پاپسیکل': 'popsickle'
    }

    @staticmethod
    def get_mongodb_client():
        """Create MongoDB client using environment settings"""
        from pymongo import MongoClient
        return MongoClient(f'mongodb://{Config.MONGODB_HOST}:{Config.MONGODB_PORT}/')
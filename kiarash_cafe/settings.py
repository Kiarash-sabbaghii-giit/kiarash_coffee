# kiarash_cafe/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import pymongo
import pyodbc

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
#   SECURITY & DEBUG
# =====================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-here-for-development-only')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# =====================================================
#   APPLICATION DEFINITION
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',

    # Local apps
    'apps.core',
    'apps.accounts',
    'apps.menu',
    'apps.orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kiarash_cafe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'kiarash_cafe.wsgi.application'

# =====================================================
#   DATABASES
# =====================================================

# ----- Django Default Database (SQLite for development) -----
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =====================================================
#   SQL SERVER CONNECTION (برای اطلاعات مشتریان و سفارشات)
# =====================================================

def get_sql_connection():
    """
    اتصال به SQL Server با Windows Authentication
    (بدون نیاز به پسورد)
    """
    try:
        # لیست درایورهای موجود را چاپ کنید تا ببینید کدام درایور در سیستم شما موجود است
        # print("Available drivers:", pyodbc.drivers())

        # تلاش با درایورهای مختلف
        drivers = [
            '{ODBC Driver 17 for SQL Server}',
            '{ODBC Driver 13 for SQL Server}',
            '{SQL Server}',
            '{SQL Server Native Client 11.0}'
        ]

        for driver in drivers:
            try:
                conn_str = (
                    f"DRIVER={driver};"
                    f"SERVER={os.getenv('DB_HOST', 'localhost\\sqlserver2025')};"
                    f"DATABASE={os.getenv('DB_NAME', 'kiarash_cafe_db')};"
                    f"Trusted_Connection=yes;"
                )
                conn = pyodbc.connect(conn_str, timeout=5)
                print(f"✅ اتصال به SQL Server با درایور {driver} برقرار شد!")
                return conn
            except Exception:
                continue

        print("❌ هیچ درایور مناسبی برای SQL Server پیدا نشد!")
        print("✅ درایورهای موجود:", pyodbc.drivers())
        return None

    except Exception as e:
        print(f"❌ خطا در اتصال به SQL Server: {e}")
        return None


# =====================================================
#   MONGODB CONNECTION (برای منو و محصولات)
# =====================================================

def get_mongodb_connection():
    """اتصال به MongoDB"""
    try:
        client = pymongo.MongoClient(
            f"mongodb://{os.getenv('MONGODB_HOST', 'localhost')}:{os.getenv('MONGODB_PORT', '27017')}/"
        )
        db = client[os.getenv('MONGODB_DATABASE', 'kiarash_cafe')]
        print("✅ اتصال به MongoDB برقرار شد!")
        return db
    except Exception as e:
        print(f"❌ خطا در اتصال به MongoDB: {e}")
        return None


# =====================================================
#   AUTHENTICATION & PASSWORD VALIDATION
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =====================================================
#   INTERNATIONALIZATION
# =====================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =====================================================
#   STATIC & MEDIA FILES
# =====================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =====================================================
#   DEFAULT PRIMARY KEY FIELD TYPE
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =====================================================
#   CRISPY FORMS
# =====================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# =====================================================
#   AUTHENTICATION
# =====================================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# =====================================================
#   SESSION
# =====================================================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours

# =====================================================
#   MESSAGES
# =====================================================

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
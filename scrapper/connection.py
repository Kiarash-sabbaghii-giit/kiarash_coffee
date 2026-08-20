import requests
from config import Config


def check_website(url=None, timeout=None):
    """Check website connection"""
    if url is None:
        url = Config.WEBSITE_URL
    if timeout is None:
        timeout = Config.REQUEST_TIMEOUT

    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ Connection to {url} successful (Status: {response.status_code})")
            return True
        else:
            print(f"⚠️ Website responded with error: {response.status_code}")
            return False
    except requests.ConnectionError:
        print(f"❌ Cannot connect to {url} (Network issue)")
        return False
    except requests.Timeout:
        print(f"❌ Connection to {url} timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_mongodb():
    """Check MongoDB connection"""
    try:
        client = Config.get_mongodb_client()
        db = client[Config.MONGODB_DATABASE]
        db.command('ping')
        print(f"✅ MongoDB connection successful at {Config.MONGODB_HOST}:{Config.MONGODB_PORT}")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False


def connect_to_mongodb():
    """Connect to MongoDB using config"""
    try:
        client = Config.get_mongodb_client()
        db = client[Config.MONGODB_DATABASE]
        print(f"✅ Connected to MongoDB at {Config.MONGODB_HOST}:{Config.MONGODB_PORT}")
        return db
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("Checking Connections:")
    print("=" * 50)
    check_website()
    check_mongodb()
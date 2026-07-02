import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv, find_dotenv  

import time
from sqlalchemy.exc import OperationalError


load_dotenv(find_dotenv())

# ================== CONFIG ==================
def get_engine():
    DB_USER = os.environ.get("MYSQL_ROOT_USER", "root")
    DB_PASS = os.environ.get("MYSQL_ROOT_PASSWORD") 
    DB_HOST = os.environ.get("MYSQL_HOST", "mysql")  
    DB_PORT = os.environ.get("MYSQL_PORT", "3306")
    DB_NAME = os.environ.get("MYSQL_DATABASE", "logistics_otd")

    if not DB_PASS:
        raise ValueError("🚨 Error: 'MYSQL_ROOT_PASSWORD' is missing in your .env file!")

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    engine = create_engine(
        connection_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_timeout=60
    )
    
    return engine

#Engine Connection Testing
if __name__ == "__main__":
    engine = get_engine()
    print("📤 Checking connection to MySQL...")
    retries = 6
    while retries > 0:
        try:
            with engine.connect() as connection:
                print("⚙️ Internal network connection successful! MySQL is ready.")
                break
        except OperationalError:
            retries -= 1
            print(f"⏳ MySQL is busy or starting up, waiting 5 seconds... ({retries} retries remaining)")
            time.sleep(5)
            
    if retries == 0:
        print("❌ Failure: Unable to connect to the database.")
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# ================== CONFIG ==================
def get_engine():
    DB_USER = os.environ.get("MYSQL_ROOT_USER", "root")
    DB_PASS = os.environ.get("MYSQL_ROOT_PASSWORD", "root123")
    DB_HOST = "mysql"  
    DB_PORT = "3306"
    DB_NAME = os.environ.get("MYSQL_DATABASE", "logistics_otd")

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


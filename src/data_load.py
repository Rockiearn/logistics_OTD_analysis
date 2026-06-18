import os
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import OperationalError

# ================== CONFIG ==================
CSV_PATH = "data/raw/SupplyChainDT.csv"

DB_USER = os.environ.get("MYSQL_ROOT_USER", "root")
DB_PASS = os.environ.get("MYSQL_ROOT_PASSWORD", "root123")
DB_HOST = "mysql"  
DB_PORT = "3306"
DB_NAME = os.environ.get("MYSQL_DATABASE", "logistics_otd")

# Tạo connection URL
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# Tối ưu Engine: Tăng kích thước bộ đệm kết nối (pool_size) để tải dữ liệu lớn nhanh hơn
engine = create_engine(
    connection_url, 
    pool_size=10, 
    max_overflow=20, 
    pool_pre_ping=True, 
    pool_timeout=60
)

def load_data():
    if not os.path.exists(CSV_PATH):
        print(f"❌ Không tìm thấy file CSV tại: {CSV_PATH}")
        print("Vui lòng đặt file CSV vào thư mục data/raw/ và kiểm tra tên file!")
        return
    
    try:
        print("📂 Đang đọc file CSV...")
        # Đọc dữ liệu
        df = pd.read_csv(CSV_PATH, encoding='latin1')
        print(f"✅ Đọc thành công! Shape: {df.shape}")
        print(f"   Số cột: {len(df.columns)}")
        
        # Kiểm tra và chờ kết nối MySQL sẵn sàng
        print("📤 Đang kiểm tra kết nối tới MySQL...")
        retries = 6
        while retries > 0:
            try:
                with engine.connect() as connection:
                    print("⚙️ Mạng nội bộ kết nối thành công! MySQL đã sẵn sàng.")
                    break
            except OperationalError:
                retries -= 1
                print(f"⏳ MySQL đang bận hoặc khởi động, đợi thêm 5 giây... (Còn {retries} lần thử)")
                time.sleep(5)
                
        if retries == 0:
            print("❌ Thất bại: Không thể kết nối đến Database.")
            return

        # Đẩy dữ liệu vào MySQL
        print("📤 Đang tiến hành nạp dữ liệu vào MySQL...")
        start_time = time.time()
        
        df.to_sql(
            name="supply_chain_raw",
            con=engine,
            if_exists="append", 
            index=False,
            chunksize=2000, 
        )
        
        end_time = time.time()
        execution_time = (end_time - start_time) / 60
        
        print("🎉 Tải toàn bộ dữ liệu thành công!")
        print(f"   Tổng số dòng đã nạp: {len(df):,}")
        print(f"   Thời gian thực thi: {execution_time:.2f} phút")
        
    except Exception as e:
        print(f"❌ Lỗi phát sinh khi load dữ liệu: {e}")

if __name__ == "__main__":
    load_data()
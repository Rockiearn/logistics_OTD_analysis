# Logistics OTD Analysis

## Problem Statement
Công ty logistics đang gặp vấn đề về **tỷ lệ giao hàng đúng hạn (On-Time Delivery - OTD)** thấp dù đã có lịch giao hàng từ trước. Dự án này nhằm phân tích nguyên nhân gốc rễ và đề xuất giải pháp cải thiện.

**Mục tiêu:**
- Tính toán và phân tích hiện trạng OTD
- Xác định các yếu tố chính gây delay (route, shipping mode, category, region...)
- Đề xuất giải pháp cụ thể kèm Projected Impact

## Dataset
- Tên: DataCo Supply Chain Dataset
- Số dòng: ~180,000
- Thời gian: 2015 - 2018

## Tech Stack
- Python (Pandas)
- MySQL
- Docker
- Git

## Project Structure

```text
.
├── data/
│   ├── processed/
│   └── raw/
│       └── SupplyChainDT.csv
├── src/
│   ├── analysis.py
│   ├── data_load.py
│   ├── eda.py
│   └── visualization.py
├── notebooks/
├── sql/
├── dashboard/
├── docker-compose.yml
├── Dockerfile
└── README.md

```

## How to Run
```bash
docker-compose up -d
docker-compose exec app python src/data_load.py (first run)
```
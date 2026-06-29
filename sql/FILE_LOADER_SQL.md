# **Database Setup & High-Performance Data Ingestion**
This directory contains the database schema and optimized scripts to ingest the Supply Chain dataset into MySQL

## Data Ingestion Strategy: to_sql vs. LOAD DATA INFILE

While Pandas' native `.to_sql()` is highly intuitive and flexible for modern Python data pipelines, it generates individual or batched `INSERT` statements under the hood. For massive production datasets, this approach introduces high overhead due to SQL parsing and network roundtrips.

As an alternative, MySQL’s native `LOAD DATA LOCAL INFILE` streams raw CSV data directly into the database engine, bypassing query parsing overhead.

## Performance Benchmark Note

For this specific dataset containing 180,519 rows and 53 columns:

- **Pandas `.to_sql()`**: ~10.8 seconds (Executed locally with memory optimization)

- **`LOAD DATA INFILE`**: ~15.5 seconds (Slower in this specific layout due to real-time `STR_TO_DATE()` mutation on 360k+ date fields during execution).

Key Takeaway: `LOAD DATA INFILE` is a specialized tool. It provides massive scaling advantages when handling multi-gigabyte files that are already pre-cleaned, where network latency or parsing overhead becomes the primary bottleneck.

## Database Configuration Setup

**1. Enable Client-Server Infile Permissions**

By default, modern MySQL servers disable local data loading due to security risks. To activate it, execute the following commands in your MySQL Client:

```
-- Check current status (if 'OFF', proceed to step 2)
SHOW VARIABLES LIKE 'local_infile';

-- Turn on local infile capability
SET GLOBAL local_infile = 1;
```

**2. Connection Settings Driver Adjustment**

To prevent access violation errors, add the local infile flag to your connection configuration:

**MySQL Workbench**: Go to Edit Connection -> Advanced -> Paste `OPT_LOCAL_INFILE=1` into the Others text box.

**Python (PyMySQL / SQLAlchemy)**: Ensure `local_infile=True` is passed into your engine connection arguments.

## Execution Guide

Execute `schema.sql` (or write the schema table creation script) to build the isolated database and initialize the target schema.

Run `load_data.sql` (containing the compiled `LOAD DATA` command) to pipe the raw CSV into the active table.
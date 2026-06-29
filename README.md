# 🚚 Logistics On-Time Delivery (OTD) Root Cause Analysis

## 📝 Open-Source Credits & Licensing

This project relies on various open-source libraries and frameworks. Below is the licensing information for the core dependencies used in the logistics analysis stack:

| Core Dependency | License Badge | License Type | Description & Usage Rights |
| :--- | :--- | :--- | :--- |
| **Python** | [![Python PSF](https://img.shields.io/badge/License-PSF-blue.svg)](https://opensource.org/licenses/Python-2.0) | PSF License | Core programming language environment. |
| **pandas** | [![Pandas BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) | BSD 3-Clause | Data manipulation, alignment, and cleaning framework. |
| **numpy** | [![NumPy BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) | BSD 3-Clause | Multidimensional array processing and numerical computing. |
| **seaborn** | [![Seaborn BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) | BSD 3-Clause | Statistical data visualization layer built on Matplotlib. |
| **matplotlib** | [![Matplotlib PSF](https://img.shields.io/badge/License-PSF_/_BSD-blue.svg)](https://matplotlib.org/stable/users/project/license.html) | PSF / BSD | Core plotting engine for generating analytical charts. |
| **SQLAlchemy** | [![SQLAlchemy MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) | MIT License | SQL Toolkit and Object-Relational Mapper (ORM) engine. |
| **PyMySQL** | [![PyMySQL MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) | MIT License | Pure-Python MySQL client library for database routing. |
| **python-dotenv** | [![Dotenv BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) | BSD 3-Clause | Secure management of database credentials via `.env` profiles. |
| **Jupyter** | [![Jupyter BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) | New BSD | Interactive computing environment for prototyping and EDA. |
| **mysql-connector** | [![MySQL GPLv2](https://img.shields.io/badge/License-GPL_v2-red.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) | GPLv2 / Comm. | Oracle's official driver for connecting Python apps to MySQL. |

### 📢 License Disclaimer
* **Permissive Stack (MIT / BSD / PSF):** The vast majority of this project's ecosystem operates under highly permissive licenses, allowing free modifications, distribution, and private or commercial deployments.
* **Copyleft Notice (GPLv2):** `mysql-connector-python` is dual-licensed under Oracle's Commercial License and the GNU General Public License v2 (GPLv2). If you choose to redistribute or commercialize this pipeline as a proprietary closed-source product, consider sticking purely to the **MIT-licensed `PyMySQL`** driver configured in `src/db_engine.py` to bypass GPL copyleft requirements.


### 📄 Project License

The core architecture, scripts, and documentation developed for this specific repository are distributed under the **MIT License**. See the `LICENSE` file in the root directory for more detailed terms.

## 💻 Tech Stack & Environment

* **Language:** Python 3.10+ (Pandas, NumPy, Matplotlib, Seaborn)
* **Database Engine:** MySQL 8.0 (Leveraging `LOAD DATA LOCAL INFILE` for optimized network ingestion performance)
* **Infrastructure:** Docker & Docker Compose for self-contained reproduction environments
* **Version Control:** Git

## 📂 Project Architecture

```text
logistics_otd_analysis/
├── data/                          # Data persistence layer
│   ├── processed/                 
│   │   ├── optimized.csv          # Optimized dataset following proposed recommendations
│   │   └── supply_chain_processed.csv
│   └── raw/                       
│       └── SupplyChainDT.csv      # Source Supply Chain dataset
├── src/                           # Modular execution script architecture
│   ├── db_engine.py               # Generates connections for the data persistence layer
│   ├── data_load.py               # Handles automated bulk loading into database
│   ├── data_processing.py         # Memory optimization, string cleanup, datetime enrichment
│   ├── eda.py                     # Initial exploratory analysis and root cause identification
│   ├── analysis.py                # Deep dive analytics (cancellations, lead time variations)
│   ├── apply_recommendations.py   # Code executing the logic transformations
│   ├── csv_optimizedfile.py       # Exports simulated post-optimization data
│   └── visualization.py           # Automated diagnostic chart plotting pipeline
├── notebooks/                     # Interactive exploratory sandboxes
│   ├── plot_customized.ipynb      
│   └── plot_testing.ipynb         
├── sql/                           # Dedicated relational queries and setups
│   ├── FILE_LOADER_SQL.md         # High-performance INFILE benchmarking vs to_sql
│   ├── load_data.sql              # Cleaned LOAD DATA LOCAL INFILE script
│   └── schema.sql                 # Data Definition Language (DDL) table schema
├── dashboard/                     # Interactive reporting app (Streamlit / Being developed)
├── visual_box/                    # Exported diagnostic chart images
├── docker-compose.yml             # Orchestration profile
├── Dockerfile                     # Environment containerization spec
├── requirements.txt               # Pinpointed dependency registry
└── README.md                      # General documentation

```

---
## 📌 Problem Statement
A global logistics provider is suffering from a critically low **On-Time Delivery (OTD) rate**, creating systemic operation bottlenecks and customer dissatisfaction despite having predetermined scheduling timelines. 

This project targets the **DataCo Supply Chain Dataset** (180,519 rows, 53 columns spanning 2015–2018) to perform deep exploratory data analysis (EDA), diagnose the structural root causes behind shipping delays, and execute data-driven optimizations to project operational improvements.



## 📊 Business Performance Diagnostics (EDA Insights)

### 1. The Core Logistics Paradox
* **The 50/50 Coin Toss:** The overall historical **OTD rate stands at a disappointing 45.17%**, while the **Late Delivery Risk reaches 54.83%**. Operationally, every two orders shipped guarantee at least one definitive delay.
* **The SLA Gap:** The average actual lead time consistently exceeds the scheduled commitment by **0.57 days**, indicating that sales-driven logistics promises systematically outpace actual fulfillment capacity.

### 2. Shipping Mode Failure Modes
Our analysis revealed that shipping channels are severely misconfigured:
* **First Class Operational Collapse:** Accounts for 15% of total volume but suffers from an unacceptable **95%+ delay rate**. 
* **Second Class Inefficiency:** Accounts for 20% of volume but sustains a **77% delay rate**.
* **The Same Day & Standard Efficiency:** In contrast, *Standard Class* (60% volume) maintains a strong 38% delay rate, and *Same Day* (5% volume) maintains a 45% delay rate under extreme time constraints.

### 3. Cascading Downstream Impacts
* **Cancellation Bottleneck:** Out of the 4.3% total canceled orders, a shocking **100% of canceled First Class orders were delayed (`is_late = 1`)**. Unrealistic shipping expectations directly trigger order cancellations.
* **Premium Pricing Fallacy:** *Second Class* and *Standard Class* display nearly identical median and mean actual lead times. Customers are paying premium rates for faster shipping but receiving standard-tier speed.
* **The Ghost Variables:** Cross-tabulations proved that product categories (e.g., *Golf Bags & Carts* with a 69% delay rate) and geographical regions (e.g., *Central Africa*, *South Asia*) only show poor OTD metrics because they have an abnormally high distribution share of *First Class* and *Second Class* shipping modes. **The true root cause is entirely systemic within the shipping modes themselves.**



## 🛠️ Data-Driven Action Plan & Proposed Recommendations

Based on the quantitative bottlenecks discovered, three structured structural shifts were modeled and applied to the data configuration:


```

┌─────────────────────────────────────────────────────────────────────────┐
│                     3-PILLAR LOGISTICS OPTIMIZATION                     │
├──────────────────────────────┬──────────────────────────────────────────┤
│ 1. Align First Class SLA     │ Increase scheduled lead time by +1 day.  │
├──────────────────────────────┼──────────────────────────────────────────┤
│ 2. Consolidate Mid-Tiers     │ Merge Second & Standard Class channels.  │
├──────────────────────────────┼──────────────────────────────────────────┤
│ 3. Bifurcate Operations      │ Split standard from expedited/same day.  │
└──────────────────────────────┴──────────────────────────────────────────┘

```

1. **SLA Alignment for First Class:** Calibrate the aggressive `scheduled lead time` expectation. Adding a single realistic buffer day shifts *First Class* from the worst performer into a highly stable 2-day delivery channel.
2. **Channel Consolidation (Decoy Elimination):** Merge *Second Class* and *Standard Class* into a single tier since processing timelines show zero statistical variance. This cuts down warehouse sorting overhead and preserves customer trust.
3. **Operational Bifurcation:** Segment logistics teams into two distinct streams: a baseline stream optimized for 2–4 day bulk processing (*Standard/First Class*) and a specialized hyper-local expedited stream (*Same Day*) focusing on regions with mature multi-hub connectivity.





## 🚀 Quick Start & Installation

### Prerequisites

* Ensure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is installed and active on your system.
* Clone this repository to your target workspace directory.

### Deployment with Docker

1. **Spin up the isolated service stack:**
```bash
docker-compose up --build -d

```


*This command provisions the Python container, installs pinned requirements, and boots the backend MySQL image simultaneously.*

2. **Run the core data pipeline:**
To execute the data ingestion, preprocessing, analysis, and simulation sequence sequentially, jump into the execution context:
```bash
docker-compose exec app python files_path

```


*(run individual files like `src/data_processing.py` or `src/apply_recommendations.py` depending on target validation workflows).*
3. **Verify Output Deliverables:**
* Review diagnostic charts populated inside `/visual_box/`.
* Access simulated target schemas via `/data/processed/optimized.csv`.



## 📓 Interactive Development with Jupyter Notebook

Since the environment is completely containerized, you can launch a Jupyter instance directly inside the active Docker application container to interact with files in the `notebooks/` directory (`plot_customized.ipynb`, `plot_testing.ipynb`).

### 1. Launch the Jupyter Server
Run the following command from your host terminal to start the notebook server attached to the container:

```bash
docker-compose exec app jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''
```

### 2. Access the Interface
Once the server initializes, you will see the active logs in your terminal:

```
[I ServerApp] [http://0.0.0.0:8888/tree](http://0.0.0.0:8888/tree)
[I ServerApp] [http://127.0.0.1:8888/tree](http://127.0.0.1:8888/tree)
```
Open your preferred web browser on your host machine and navigate to either:

👉 http://localhost:8888

👉 http://127.0.0.1:8888

(Note: The token authentication flag --NotebookApp.token='' has been set to empty for frictionless local prototyping, meaning no password is required to access the UI).
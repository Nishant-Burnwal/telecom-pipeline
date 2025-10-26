Automated Network Performance Data Pipeline for Telecom Insights.
Project scaffold for ETL: extract → clean → analyze → export.

Telecom Data Pipeline
A complete end-to-end data pipeline project for processing and analyzing telecom network performance metrics using Python, MySQL, and GitHub Actions.

Overview
This project automates the ETL (Extract, Transform, Load) process for telecom data. It collects raw network logs, transforms them into a clean format, loads the results into a MySQL database, and schedules the pipeline automatically using GitHub Actions.

Features
Automated ETL execution using GitHub Actions

MySQL integration for structured data storage

Data cleaning and transformation using pandas

Configurable database connection via .env file

Hourly or daily scheduling using cron jobs

Tech Stack
Python 3.10+

MySQL 8.0

pandas, SQLAlchemy, dotenv

GitHub Actions for CI/CD automation

Project Structure
telecom-pipeline/
│
├── src/
│   ├── pipeline.py           # ETL script
│   ├── db.py                 # MySQL connection and helper functions
│
├── .env                      # Environment variables (ignored by git)
├── requirements.txt
├── .github/
│   └── workflows/
│       ├── pipeline.yml      # ETL automation workflow
│       └── etl_automation.yml# Optional hourly scheduled workflow
└── README.md

Setup Instructions

1. Clone the Repository
git clone https://github.com/<your-username>/telecom-pipeline.git
cd telecom-pipeline


2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt


3. Configure Database Connection
Create a .env file in the root directory:
ini
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=telecom_db
MYSQL_USER=root
MYSQL_PASSWORD=your_password


4. Run the ETL Pipeline
python src/pipeline.py
GitHub Actions Automation
The project uses two workflows:

pipeline.yml
Runs the ETL pipeline automatically whenever you push to the main branch.

etl_automation.yml
Uses a cron schedule (0 * * * *) to execute the ETL every hour automatically.

MySQL runs as a service inside GitHub Actions for testing the entire process.
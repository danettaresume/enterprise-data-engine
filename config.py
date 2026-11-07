import os
API_URL = os.getenv("API_URL", "https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json&per_page=100")
DB_PATH = os.getenv("DB_PATH", "output/economic_data.db")
REPORT_PATH = os.getenv("REPORT_PATH", "output/dashboard.html")

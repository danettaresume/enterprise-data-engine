# Enterprise Data Engine

A small end-to-end ETL reference application using the World Bank's public US GDP API. It fetches JSON, validates/normalizes records, stores them in SQLite, and generates an HTML dashboard.

## Run

```bash
python -m pip install -r requirements.txt
python pipeline.py
python -m pytest
```

Open `output/dashboard.html`. The pipeline requires internet access. Customize `API_URL`, `DB_PATH`, and `REPORT_PATH` using environment variables. Docker: `docker build -t enterprise-data-engine . && docker run --rm -v "$(pwd)/output:/app/output" enterprise-data-engine` (on Windows, adapt the volume syntax).

## Notes

This is a reference implementation, not a claim of production deployment. Data source: World Bank API, NY.GDP.MKTP.CD. API data can change and the latest available year may lag the current year.

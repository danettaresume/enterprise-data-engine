import html
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import requests
from config import API_URL, DB_PATH, REPORT_PATH

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

def fetch(url=API_URL):
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2 or not isinstance(payload[1], list):
        raise ValueError("Unexpected World Bank response")
    return payload[1]

def normalize(records):
    clean = []
    for item in records:
        if not isinstance(item, dict) or item.get("value") is None:
            continue
        try:
            year = int(item["date"])
            value = float(item["value"])
        except (KeyError, TypeError, ValueError):
            continue
        clean.append((year, value))
    return sorted(set(clean), reverse=True)

def save(rows, path=DB_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS gdp (year INTEGER PRIMARY KEY, value REAL NOT NULL)")
        conn.executemany("INSERT OR REPLACE INTO gdp(year,value) VALUES (?,?)", rows)

def report(rows, path=REPORT_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    latest = rows[0] if rows else None
    headline = f"${latest[1]/1e12:,.2f} trillion ({latest[0]})" if latest else "No data"
    body = "".join(f"<tr><td>{year}</td><td>${value:,.0f}</td></tr>" for year,value in rows)
    stamp = html.escape(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))
    page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><title>US GDP Dashboard</title>
    <style>body{{font-family:Arial,sans-serif;max-width:850px;margin:3rem auto;padding:1rem;color:#17243b}}table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #ddd;text-align:left}}h1{{color:#173b70}}</style>
    <h1>US GDP Data Dashboard</h1><p>Latest reported GDP: <strong>{headline}</strong></p>
    <p>Records: {len(rows)} | Generated: {stamp}</p><table><tr><th>Year</th><th>GDP (current US$)</th></tr>{body}</table>
    <p>Source: World Bank API, indicator NY.GDP.MKTP.CD</p></html>"""
    Path(path).write_text(page, encoding="utf-8")

def main():
    rows = normalize(fetch())
    if not rows:
        raise RuntimeError("No usable GDP data returned")
    save(rows)
    report(rows)
    logging.info("Saved %s GDP records and generated %s", len(rows), REPORT_PATH)

if __name__ == "__main__":
    main()

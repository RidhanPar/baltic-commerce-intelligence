"""Load generated CSVs into dbt's SQLite raw source database."""
import csv
import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
db = root / "data" / "processed" / "dbt_analytics.db"
conn = sqlite3.connect(db)
for name in ["prospects", "customers", "orders"]:
    with (root / "data" / "raw" / f"{name}.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    columns = list(rows[0])
    conn.execute(f"drop table if exists {name}")
    conn.execute(f"create table {name} ({', '.join(column + ' text' for column in columns)})")
    conn.executemany(f"insert into {name} values ({','.join('?' for _ in columns)})", [[row[column] for column in columns] for row in rows])
conn.commit()
conn.close()

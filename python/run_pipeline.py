"""Build the analytical warehouse, analysis outputs, dashboard, and Excel report."""

from __future__ import annotations

import argparse
import csv
import html
import sqlite3
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill

TABLE_FILES = {
    "dim_customer": "customers.csv",
    "fct_orders": "orders.csv",
    "fct_marketing_spend": "marketing_spend.csv",
    "fct_deliveries": "deliveries.csv",
    "fct_experiment_assignments": "experiment_assignments.csv",
}


def load_csv(conn: sqlite3.Connection, table: str, path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    columns = list(rows[0])
    conn.execute(f"DROP TABLE IF EXISTS {table}")
    conn.execute(f"CREATE TABLE {table} ({', '.join(f'{column} TEXT' for column in columns)})")
    placeholders = ", ".join("?" for _ in columns)
    conn.executemany(
        f"INSERT INTO {table} VALUES ({placeholders})",
        [[row[column] for column in columns] for row in rows],
    )


def build_marts(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP VIEW IF EXISTS mart_channel_profitability;
        CREATE VIEW mart_channel_profitability AS
        SELECT
            acquisition_channel,
            COUNT(DISTINCT order_id) AS orders,
            COUNT(DISTINCT customer_id) AS customers,
            ROUND(SUM(CAST(net_revenue AS REAL)), 2) AS net_revenue,
            ROUND(SUM(CAST(contribution_margin AS REAL)), 2) AS contribution_margin,
            ROUND(SUM(CAST(contribution_margin AS REAL)) / NULLIF(SUM(CAST(net_revenue AS REAL)), 0), 4)
                AS contribution_margin_pct,
            ROUND(AVG(CAST(contribution_margin AS REAL)), 2) AS contribution_margin_per_order
        FROM fct_orders
        WHERE order_status = 'completed'
        GROUP BY acquisition_channel;

        DROP VIEW IF EXISTS mart_market_profitability;
        CREATE VIEW mart_market_profitability AS
        SELECT
            market,
            COUNT(DISTINCT order_id) AS orders,
            ROUND(SUM(CAST(net_revenue AS REAL)), 2) AS net_revenue,
            ROUND(SUM(CAST(contribution_margin AS REAL)), 2) AS contribution_margin,
            ROUND(AVG(CAST(contribution_margin AS REAL)), 2) AS contribution_margin_per_order
        FROM fct_orders
        WHERE order_status = 'completed'
        GROUP BY market;

        DROP VIEW IF EXISTS mart_logistics;
        CREATE VIEW mart_logistics AS
        SELECT
            carrier,
            COUNT(*) AS deliveries,
            ROUND(AVG(CAST(on_time AS REAL)), 4) AS on_time_rate,
            ROUND(AVG(CAST(delivery_cost AS REAL)), 2) AS avg_delivery_cost
        FROM fct_deliveries
        GROUP BY carrier;

        DROP VIEW IF EXISTS mart_experiment;
        CREATE VIEW mart_experiment AS
        SELECT
            e.treatment,
            COUNT(DISTINCT e.customer_id) AS assigned_customers,
            ROUND(AVG(COALESCE(o.customer_margin, 0)), 2) AS margin_per_assigned_customer,
            ROUND(AVG(CASE WHEN COALESCE(o.order_count, 0) > 0 THEN 1.0 ELSE 0 END), 4) AS conversion_rate
        FROM fct_experiment_assignments e
        LEFT JOIN (
            SELECT customer_id,
                   SUM(CAST(contribution_margin AS REAL)) AS customer_margin,
                   COUNT(*) AS order_count
            FROM fct_orders
            WHERE order_status = 'completed'
            GROUP BY customer_id
        ) o USING (customer_id)
        GROUP BY e.treatment;
        """
    )


def query_rows(conn: sqlite3.Connection, query: str) -> list[dict]:
    cursor = conn.execute(query)
    columns = [item[0] for item in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def write_csv_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def bar_svg(rows: list[dict], label: str, metric: str, color: str) -> str:
    values = [float(row[metric]) for row in rows]
    maximum = max(abs(value) for value in values)
    zero_x = 390
    items = []
    for index, row in enumerate(rows):
        value = float(row[metric])
        width = 310 * abs(value) / maximum if maximum else 0
        x = zero_x if value >= 0 else zero_x - width
        fill = color if value >= 0 else "#dc2626"
        value_x = x + width + 10 if value >= 0 else x - 58
        y = 12 + index * 46
        items.append(
            f'<text x="0" y="{y + 18}" class="label">{html.escape(str(row[label]))}</text>'
            f'<line x1="{zero_x}" x2="{zero_x}" y1="{y - 4}" y2="{y + 30}" stroke="#94a3b8"/>'
            f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="25" rx="4" fill="{fill}"/>'
            f'<text x="{value_x:.1f}" y="{y + 18}" class="value">{value:,.1f}</text>'
        )
    return f'<svg viewBox="0 0 760 {len(rows) * 46 + 12}" role="img">{"".join(items)}</svg>'


def build_dashboard(output: Path, channels: list[dict], logistics: list[dict], summary: dict) -> None:
    channel_chart = bar_svg(channels, "acquisition_channel", "contribution_margin", "#2563eb")
    logistics_chart = bar_svg(logistics, "carrier", "on_time_rate", "#0f766e")
    output.write_text(
        f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Baltic Commerce Intelligence</title>
<style>
body{{font-family:Arial,sans-serif;margin:0;background:#f4f7fb;color:#172033}}
main{{max-width:1120px;margin:auto;padding:36px}} h1{{font-size:34px;margin-bottom:8px}}
.sub{{color:#60708a;margin-bottom:28px}} .cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.card,.panel{{background:white;border-radius:12px;padding:20px;box-shadow:0 5px 18px #1e293b12}}
.metric{{font-size:27px;font-weight:bold;color:#163a70}} .label{{font-size:13px;fill:#334155}} .value{{font-size:12px;fill:#475569}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:22px}} svg{{width:100%;height:auto}}
table{{width:100%;border-collapse:collapse}} th,td{{padding:9px;border-bottom:1px solid #e2e8f0;text-align:left}}
@media(max-width:800px){{.cards,.grid{{grid-template-columns:1fr 1fr}}}}
</style></head><body><main>
<h1>Baltic Commerce Intelligence</h1><div class="sub">Profitable growth portfolio dashboard | Synthetic 2025 data</div>
<section class="cards">
<div class="card"><div>Total orders</div><div class="metric">{summary['orders']:,}</div></div>
<div class="card"><div>Net revenue</div><div class="metric">€{summary['net_revenue']:,.0f}</div></div>
<div class="card"><div>Contribution margin</div><div class="metric">€{summary['contribution_margin']:,.0f}</div></div>
<div class="card"><div>Margin rate</div><div class="metric">{summary['margin_rate']:.1%}</div></div>
</section>
<section class="grid">
<div class="panel"><h2>Contribution margin by channel</h2>{channel_chart}</div>
<div class="panel"><h2>On-time delivery rate by carrier</h2>{logistics_chart}</div>
</section>
<section class="panel" style="margin-top:22px"><h2>Channel profitability detail</h2><table>
<tr><th>Channel</th><th>Orders</th><th>Net revenue</th><th>Contribution margin</th><th>Margin %</th></tr>
{''.join(f"<tr><td>{r['acquisition_channel']}</td><td>{r['orders']:,}</td><td>€{r['net_revenue']:,.0f}</td><td>€{r['contribution_margin']:,.0f}</td><td>{r['contribution_margin_pct']:.1%}</td></tr>" for r in channels)}
</table></section></main></body></html>""",
        encoding="utf-8",
    )


def build_excel(output: Path, channels: list[dict], markets: list[dict], logistics: list[dict]) -> None:
    workbook = Workbook()
    summary = workbook.active
    summary.title = "Executive Summary"
    summary.append(["Baltic Commerce Intelligence", "2025 synthetic portfolio data"])
    summary["A1"].font = Font(size=18, bold=True, color="FFFFFF")
    summary["A1"].fill = PatternFill("solid", fgColor="163A70")
    summary.merge_cells("A1:E1")
    summary.append([])
    summary.append(["Channel", "Orders", "Net Revenue", "Contribution Margin", "Margin %"])
    for row in channels:
        summary.append(
            [
                row["acquisition_channel"],
                row["orders"],
                row["net_revenue"],
                row["contribution_margin"],
                row["contribution_margin_pct"],
            ]
        )
    chart = BarChart()
    chart.title = "Contribution Margin by Channel"
    chart.add_data(Reference(summary, min_col=4, min_row=3, max_row=3 + len(channels)), titles_from_data=True)
    chart.set_categories(Reference(summary, min_col=1, min_row=4, max_row=3 + len(channels)))
    summary.add_chart(chart, "G3")

    for title, rows in [("Market Detail", markets), ("Logistics Detail", logistics)]:
        sheet = workbook.create_sheet(title)
        sheet.append(list(rows[0]))
        for row in rows:
            sheet.append(list(row.values()))
        for cell in sheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="2563EB")
    output.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output)


def run(root: Path) -> None:
    raw = root / "data" / "raw"
    processed = root / "data" / "processed"
    artifacts = root / "artifacts"
    processed.mkdir(parents=True, exist_ok=True)
    artifacts.mkdir(parents=True, exist_ok=True)
    database = processed / "analytics.db"
    conn = sqlite3.connect(database)
    for table, filename in TABLE_FILES.items():
        load_csv(conn, table, raw / filename)
    build_marts(conn)

    channels = query_rows(conn, "SELECT * FROM mart_channel_profitability ORDER BY contribution_margin DESC")
    markets = query_rows(conn, "SELECT * FROM mart_market_profitability ORDER BY contribution_margin DESC")
    logistics = query_rows(conn, "SELECT * FROM mart_logistics ORDER BY on_time_rate DESC")
    experiment = query_rows(conn, "SELECT * FROM mart_experiment ORDER BY treatment")
    summary = query_rows(
        conn,
        """SELECT COUNT(*) orders, ROUND(SUM(CAST(net_revenue AS REAL)),2) net_revenue,
        ROUND(SUM(CAST(contribution_margin AS REAL)),2) contribution_margin,
        SUM(CAST(contribution_margin AS REAL))/SUM(CAST(net_revenue AS REAL)) margin_rate
        FROM fct_orders WHERE order_status='completed'""",
    )[0]
    for name, rows in [("channel_profitability", channels), ("market_profitability", markets), ("logistics", logistics), ("experiment", experiment)]:
        write_csv_rows(processed / f"{name}.csv", rows)
    build_dashboard(artifacts / "dashboard.html", channels, logistics, summary)
    build_excel(artifacts / "finance_analysis.xlsx", channels, markets, logistics)
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    run(args.root)

import csv
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from generate_data import generate
from run_pipeline import run


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        generate(self.root / "data" / "raw", seed=11, customer_count=200)
        run(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_orders_have_unique_ids(self):
        with (self.root / "data" / "raw" / "orders.csv").open(newline="", encoding="utf-8") as handle:
            ids = [row["order_id"] for row in csv.DictReader(handle)]
        self.assertEqual(len(ids), len(set(ids)))

    def test_completed_orders_reconcile(self):
        conn = sqlite3.connect(self.root / "data" / "processed" / "analytics.db")
        raw_total = conn.execute(
            "SELECT ROUND(SUM(CAST(contribution_margin AS REAL)), 2) FROM fct_orders WHERE order_status='completed'"
        ).fetchone()[0]
        mart_total = conn.execute(
            "SELECT ROUND(SUM(contribution_margin), 2) FROM mart_channel_profitability"
        ).fetchone()[0]
        conn.close()
        self.assertAlmostEqual(raw_total, mart_total, places=2)

    def test_artifacts_created(self):
        self.assertTrue((self.root / "artifacts" / "dashboard.html").exists())
        self.assertTrue((self.root / "artifacts" / "finance_analysis.xlsx").exists())

    def test_dashboard_has_no_negative_svg_widths(self):
        dashboard = (self.root / "artifacts" / "dashboard.html").read_text(encoding="utf-8")
        self.assertNotIn('width="-', dashboard)


if __name__ == "__main__":
    unittest.main()

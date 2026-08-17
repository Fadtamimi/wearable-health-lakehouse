from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepoLayoutTest(unittest.TestCase):
    def test_core_files_exist(self):
        expected = [
            ROOT / "README.md",
            ROOT / "requirements.txt",
            ROOT / "dags" / "wearable_health_lakehouse_dag.py",
            ROOT / "scripts" / "01_bronze_to_silver.py",
            ROOT / "scripts" / "02_silver_to_gold.py",
        ]
        for path in expected:
            self.assertTrue(path.exists(), f"Missing file: {path}")


if __name__ == "__main__":
    unittest.main()


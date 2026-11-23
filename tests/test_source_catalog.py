import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def test_all_versions_covered(self):
        groups = json.loads((ROOT / 'config/sources.json').read_text(encoding='utf-8'))
        sim = {g['version'] for g in groups if g['family'] == 'isaac_sim'}
        self.assertEqual(sim, {'5.1.0', '6.0.0', '6.0.1', '6.1.0', '6.2.0'})
        lab = {g['version'] for g in groups if g['family'] == 'isaac_lab'}
        self.assertTrue(sim.issubset(lab))

    def test_official_domains_and_catalog(self):
        groups = json.loads((ROOT / 'config/sources.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(groups), 15)
        for g in groups:
            self.assertTrue(g['base'].startswith('https://'))
            self.assertGreater(len(g['seeds']), 0)
            self.assertGreater(g['max_pages'], 5)


if __name__ == '__main__':
    unittest.main()

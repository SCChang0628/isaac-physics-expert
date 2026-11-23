import unittest
from expert.common import chunks


class ChunkTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(chunks("\n\t"), [])

    def test_roundtrip_simple(self):
        self.assertEqual(chunks("Physics Solver Setting."), ["Physics Solver Setting."])

    def test_chunk_bounds(self):
        res = chunks("a" * 5000, size=1000, overlap=100)
        self.assertGreater(len(res), 1)
        self.assertTrue(all(len(v) <= 1000 for v in res))


if __name__ == "__main__":
    unittest.main()

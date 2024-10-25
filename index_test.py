from index import GenStrAsmIdx
from parameterized import parameterized
import unittest

class TestIndex(unittest.TestCase):

    @parameterized.expand([
        ["sdfsdf", 3],
        ["sdfsdfsdfsdf", 4],
        ["abracadabra", 7],
        ["hello world", 10],
        ["threeintree", 8],
        ["wood chuck chuck", 10],
    ])
    def testGenStrAsmIdx(self, s, idx):
        hist = list(GenStrAsmIdx(s))[-1]
        self.assertIsNotNone(hist)
        self.assertEqual(hist.asm_idx, idx)

if __name__ == '__main__':
    unittest.main()

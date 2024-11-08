from assembly import *
from index import *
from parameterized import parameterized
import unittest

class TestIndex(unittest.TestCase):

    @parameterized.expand([
        ['sdfsdf', 3],
        ['sdfsdfsdfsdf', 4],
        ['ababacac', 5],
        ['abacacab', 5],
        ['abracadabra', 7],
        ['wod_chuck_chuck', 9]
    ])
    def testGenStrAsmIdx(self, s, idx):
        hist = list(GenStrAsmIdx(s))[-1]
        self.assertIsNotNone(hist)
        self.assertEqual(hist.asm_idx, idx)
        cache = StrAsmIdxCache(hist.asm, hist, None)
        self.assertEqual(cache.min_steps_left, 0)

    @parameterized.expand([
        ['a', 'abracadabra', 4, 3],
        ['c', 'abracadabra', 4, 3],
        ['aaaaa', 'abracadabra', 4, 1],
        ['abracadabra', 'abracadabra', 0, 0],
        ['abrcdabra', 'abracadabra', 0, 1],
        ['abcdd', 'abcdabcdabcd', 0, 2],
    ])
    def testMinStepsLeft(self, a, s, breadth, depth):
        steps = breadth + depth
        start = StringAssembly.Create(a)
        target = StringAssembly.Create(s)
        hist = History(AsmCtor(start), None, {start})
        cache = StrAsmIdxCache(target, hist, None, check_sub=False)
        self.assertEqual(cache.breadth_left, breadth)
        self.assertEqual(cache.depth_left, depth)
        self.assertEqual(cache.min_steps_left, steps)

if __name__ == '__main__':
    unittest.main()

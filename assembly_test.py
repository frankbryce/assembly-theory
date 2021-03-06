import assembly
from parameterized import parameterized
import unittest

class TestPath(unittest.TestCase):

    @parameterized.expand([
        ["sdfsdf", 3],
        ["sdfsdfsdfsdf", 4],
        ["abracadabra", 7],
        ["hello world", 10],
        ["iseethreeintree", 11],
        ["abeeceedeeeeffgee", 12],
    ])
    def testMinStrPaths(self, s, idx):
        paths = assembly.MinStrPaths(s)
        self.assertNotEqual(len(paths), 0)
        for path in paths:
            self.assertEqual(path.Index(), idx)

if __name__ == '__main__':
    unittest.main()

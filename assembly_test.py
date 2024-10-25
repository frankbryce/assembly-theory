from assembly import History, AtomCtor, StrAppendCtor, StrAtom
# from parameterized import parameterized
import unittest

class TestPath(unittest.TestCase):

    def testStringConcat(self):
        a = StrAtom('a')
        b = StrAtom('b')
        aa = a.Append(a)
        self.assertEqual(str(aa), 'aa')
        aaa = a.Append(aa)
        self.assertEqual(str(aaa), 'aaa')
        aaab = aaa.Append(b)
        self.assertEqual(str(aaab), 'aaab')
        aaabaaa = aaab.Append(aaa)
        self.assertEqual(str(aaabaaa), 'aaabaaa')

    def testStringAssembly(self):
        a = StrAtom('a')
        b = StrAtom('b')
        r = StrAtom('r')
        c = StrAtom('c')
        d = StrAtom('d')
        ab = a.Append(b)
        self.assertEqual(str(ab), 'ab')
        abr = ab.Append(r)
        self.assertEqual(str(abr), 'abr')
        abra = abr.Append(a)
        self.assertEqual(str(abra), 'abra')
        abrac = abra.Append(c)
        self.assertEqual(str(abrac), 'abrac')
        abraca = abrac.Append(a)
        self.assertEqual(str(abraca), 'abraca')
        abracad = abraca.Append(d)
        self.assertEqual(str(abracad), 'abracad')
        abracadabra = abracad.Append(abra)
        self.assertEqual(str(abracadabra), 'abracadabra')

    def testGenerateAbracadabraHistory(self):
        a = History(AtomCtor, StrAtom('a'))
        b = History(AtomCtor, StrAtom('b'))
        r = History(AtomCtor, StrAtom('r'))
        c = History(AtomCtor, StrAtom('c'))
        d = History(AtomCtor, StrAtom('d'))
        ab = History(StrAppendCtor, b, parent=a)
        abr = History(StrAppendCtor, r, parent=ab)
        abra = History(StrAppendCtor, a, parent=abr)
        abrac = History(StrAppendCtor, c, parent=abra)
        abraca = History(StrAppendCtor, a, parent=abrac)
        abracad = History(StrAppendCtor, d, parent=abraca)
        abracadabra = History(StrAppendCtor, abra, parent=abracad)
        self.assertEqual(str(abracadabra.asm), 'abracadabra')
        self.assertEqual(abracadabra.asm_idx, 7)

    # @parameterized.expand([
    #     ["sdfsdf", 3],
    #     ["sdfsdfsdfsdf", 4],
    #     ["abracadabra", 7],
    #     ["hello world", 10],
    #     ["iseethreeintree", 11],
    #     ["abeeceedeeeeffgee", 12],
    # ])
    # def testMinStrPaths(self, s, idx):
    #     paths = assembly.MinStrPaths(s)
    #     self.assertNotEqual(len(paths), 0)
    #     for path in paths:
    #         self.assertEqual(path.Index(), idx)

if __name__ == '__main__':
    unittest.main()

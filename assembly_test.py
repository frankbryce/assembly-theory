from assembly import *
from itertools import product
from parameterized import parameterized
import unittest

class TestAssembly(unittest.TestCase):

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
        self.assertEqual(aaabaaa.el_cnts, {'a': 6, 'b': 1})

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
        a = History(AsmCtor(StrAtom('a')))
        b = History(AsmCtor(StrAtom('b')))
        r = History(AsmCtor(StrAtom('r')))
        c = History(AsmCtor(StrAtom('c')))
        d = History(AsmCtor(StrAtom('d')))
        ab = History(StrAppendCtor(b), parent=a)
        abr = History(StrAppendCtor(r), parent=ab)
        abra = History(StrAppendCtor(a), parent=abr)
        abrac = History(StrAppendCtor(c), parent=abra)
        abraca = History(StrAppendCtor(a), parent=abrac)
        abracad = History(StrAppendCtor(d), parent=abraca)
        abracadabra = History(StrAppendCtor(abra), parent=abracad)
        self.assertEqual(str(abracadabra.asm), 'abracadabra')
        self.assertEqual(abracadabra.asm_idx, 7)
        self.assertEqual(abracadabra.asm.el_cnts, {'a': 5, 'b': 2, 'c': 1, 'd': 1, 'r': 2})

    @parameterized.expand([
        [[History(AsmCtor(StrAtom('a'))),
         History(AsmCtor(StrAtom('b'))),
         History(AsmCtor(StrAtom('r'))),
         History(AsmCtor(StrAtom('c'))),
         History(AsmCtor(StrAtom('d')))], StrAppendAsmCtor],
    ])
    def testUniqueHashes(self, asms, ctor):
        hashes = set()
        for asm in asms:
            self.assertNotIn(asm.__hash__(), hashes)
            hashes.add(asm.__hash__())
        
        for asm1, asm2 in product(asms, repeat=2):
            hist = History(ctor(asm1.asm, asm2.asm), parent=asm1)
            self.assertNotIn(hist.__hash__(), hashes)
            hashes.add(hist.__hash__())

if __name__ == '__main__':
    unittest.main()

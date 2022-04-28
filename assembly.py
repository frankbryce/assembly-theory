from __future__ import annotations

class Path:
    obj: str
    bks: set[Path]  # for caching only
    left: Path
    right: Path

    def __init__(self, obj: str, left: Path, right: Path) -> Path:
        self.obj = obj
        self.left = left
        self.right = right
        if (not left and right) or (left and not right):
            raise ValueError('must specify both left and right, or neither.')
        self.bks = set([self])
        if left:
            self.bks |= left.bks
            self.bks |= right.bks

    def __eq__(self, other: Path) -> bool:
        return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash(self.obj)

    def __str__(self) -> str:
        return f'index of {self.Index()}: {self.obj}'

    def Index(self, exists: set[Path] = set()) -> int:
        l = self.left
        r = self.right
        if (not l and r) or (l and not r):
            raise ValueError('Invalid State: had only one of self.left and self.right set')
        if not l and not r:
            return 0  # this is an atom

        # assemble right from left's building blocks
        lr_idx = 1  # take into account this assembly step.
        if l not in exists:
            lr_idx += l.Index()
        lr_idx += r.Index(exists | l.bks)

        # assemble left from right's building blocks
        rl_idx = 1
        if r not in exists:
            rl_idx += r.Index()
        rl_idx += l.Index(exists | r.bks)

        return min(lr_idx, rl_idx)

    def raw(self, concat: str = '|', lbr: str = '(', rbr: str = ')') -> str:
        return self.obj.translate({ord(lbr): None, ord(rbr): None, ord(concat): None})

    @staticmethod
    def Atom(s: str) -> Path:
        return Path(s, None, None)

    @staticmethod
    def From(left: Path, right: Path, concat: str = '|', lbr: str = '(', rbr: str = ')') -> Path:
        return Path(f'{lbr}{left.obj}{concat}{right.obj}{rbr}', left, right)

def MinStrPaths(s: str) -> list[Path]:
    layers: list[set[Path]] = list()
    atoms = set([Path.Atom(c) for c in s])
    layers.append(atoms)
    for l in range(1,len(s)):
        next_layer = set()
        for i in range(int((l+1)/2)):
            l1 = layers[i]
            l2 = layers[l-i-1]
            next_layer |= set([Path.From(o1,o2) for o1 in l1 for o2 in l2 if o1.raw()+o2.raw() in s])
        layers.append(next_layer)
    
    minPaths = list()
    minIdx = len(s)+1
    for path in layers[len(s)-1]:
        pidx = path.Index()
        if pidx < minIdx:
            minIdx = pidx
            minPaths = [path]
        elif pidx == minIdx:
            minPaths.append(path)
    return minPaths

def genearateAbracadabra() -> Path:
    # generate and return the Path that represents 'abracadabra'
    a = Path.Atom('a') # idx = 0
    b = Path.Atom('b') # idx = 0
    r = Path.Atom('r') # idx = 0
    c = Path.Atom('c') # idx = 0
    d = Path.Atom('d') # idx = 0
    ab = Path.From(a,b) # idx = 1
    abr = Path.From(ab,r) # idx = 2
    abra = Path.From(abr,a) # idx = 3
    abrac = Path.From(abra,c) # idx = 4
    abraca = Path.From(abrac,a) # idx = 5
    abracad = Path.From(abraca,d) # idx = 6
    abracadabra = Path.From(abracad,abra) # idx = 7
    print(abracadabra)

if __name__ == "__main__":
    print("print all min assembly paths for 'abracadabra'")
    for path in MinStrPaths('abracadabra'):
        print(path)

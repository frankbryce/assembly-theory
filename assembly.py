from __future__ import annotations

from functools import cache
import sys
from tqdm import tqdm

class Assembly:
    val: str

    def __init__(self, val) -> Assembly:
        self.val = val

    def __lt__(self, other: Assembly) -> bool:
        return self.val < other.val

    def __eq__(self, other: Assembly) -> bool:
        return self.val == other.val
        
    def __hash__(self):
        return hash(self.val)

    def __str__(self) -> str:
        return self.val

class Path:
    idx: int
    obj: Assembly
    bks: set[Assembly]  # cache of blocks used to build this path
    left: Path
    right: Path

    # construct Path from adding an object "right"
    def __init__(self, obj: Assembly, left: Path, right: Path) -> Path:
        self.obj = obj
        self.left = left
        self.right = right
        if (not left and right) or (left and not right):
            raise ValueError('must specify both left and right, or neither.')
        self.bks = set([obj])
        if left:
            self.bks |= left.bks
            self.bks |= right.bks

        if not left:
            self.idx = 0  # this is an atom
        else:
            # assemble right from left's building blocks
            lr_idx = 1  # take into account this assembly step.
            lr_idx += left.idx
            lr_idx += right.Index(tuple(sorted(left.bks)))
    
            # assemble left from right's building blocks
            rl_idx = 1
            rl_idx += right.idx
            rl_idx += left.Index(tuple(sorted(right.bks)))

            self.idx = min(lr_idx, rl_idx)

    def __eq__(self, other: Path) -> bool:
        return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash((self.obj,tuple(sorted(self.bks))))

    def __str__(self) -> str:
        return f'{self.idx}:{self.obj}'

    @cache
    def Index(self, exists: tuple[Assembly] = tuple()) -> int:
        l = self.left
        r = self.right
        if (not l and r) or (l and not r):
            raise ValueError('Invalid State: had only one of self.left and self.right set')
        if not l and not r:
            return 0  # this is an atom

        # assemble right from left's building blocks
        lr_idx = 1  # take into account this assembly step.
        if l.obj not in exists:
            lr_idx += l.idx
        lr_idx += r.Index(tuple(sorted(exists + tuple(l.bks))))

        # assemble left from right's building blocks
        rl_idx = 1
        if r.obj not in exists:
            rl_idx += r.idx
        rl_idx += l.Index(tuple(sorted(exists + tuple(r.bks))))

        return min(lr_idx, rl_idx)

    @staticmethod
    def Atom(s: str) -> Path:
        return Path(Assembly(s), None, None)

    @staticmethod
    def Join(left: Path, right: Path, concat: str = '', lbr: str = '', rbr: str = '') -> Path:
        val = f'{lbr}{left.obj}{concat}{right.obj}{rbr}'
        return Path(Assembly(val), left, right)

def MinStrPaths(s: str) -> list[Path]:
    layers: list[set[Path]] = list()
    atoms = set([Path.Atom(c) for c in s])
    layers.append(atoms)
    for l in tqdm(range(1,len(s)), "Generating Paths: "):
        next_layer = set()
        for i in range(int((l+1)/2)):
            l1 = layers[i]
            l2 = layers[l-i-1]
            next_layer |= set([Path.Join(o1,o2) for o1 in l1 for o2 in l2 if str(o1.obj)+str(o2.obj) in s])
        layers.append(next_layer)
    
    minPaths = list()
    minIdx = len(s)+1
    for path in tqdm(layers[len(s)-1], "Looking for min index"):
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
    ab = Path.Join(a,b) # idx = 1
    abr = Path.Join(ab,r) # idx = 2
    abra = Path.Join(abr,a) # idx = 3
    abrac = Path.Join(abra,c) # idx = 4
    abraca = Path.Join(abrac,a) # idx = 5
    abracad = Path.Join(abraca,d) # idx = 6
    abracadabra = Path.Join(abracad,abra) # idx = 7
    print(abracadabra)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        assemble_str = 'abracadabra'
    else:
        assemble_str = sys.argv[1]
    print(f"print all min assembly paths for '{assemble_str}'")
    for path in MinStrPaths(assemble_str):
        print(path)


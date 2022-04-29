from __future__ import annotations

from functools import lru_cache
cache = lru_cache(maxsize=None)
import networkx as nx
import sys
from tqdm import tqdm

class Assembly:
    atoms: nx.MultiGraph

    @staticmethod
    def Atom(element: str):
        ret = Assembly()
        ret.atoms = nx.MultiGraph()
        ret.atoms.add_nodes_from([(0, {'element': element})])
        return ret

    @staticmethod
    def Concat(left: Assembly, right: Assembly) -> Assembly:
        ret = Assembly()
        lsz = len(left.atoms)
        rsz = len(right.atoms)
        rcpy = right.atoms.copy()
        nx.relabel_nodes(rcpy, dict([(i,i+lsz) for i in range(rsz)]), copy=False)
        ret.atoms = nx.compose(left.atoms,rcpy)
        ret.atoms.add_edge(lsz-1,lsz)
        return ret

    def is_atom(self) -> bool:
        return len(self.atoms) == 1

    def __lt__(self, other: Assembly) -> bool:
        return self.__hash__() < other.__hash__()

    def __eq__(self, other: Assembly) -> bool:
        return self.__hash__() == other.__hash__()
        
    def __hash__(self):
        return int(nx.weisfeiler_lehman_graph_hash(self.atoms, node_attr='element'),16)

    def __str__(self) -> str:
        return ''.join([a['element'] for _,a in sorted(self.atoms.nodes(data=True), key=lambda n: n[0])])

class Path:
    idx: int
    asm: Assembly
    bks: set[Assembly]  # cache of blocks used to build this path
    left: Path
    right: Path

    def __init__(self, asm: Assembly, left: Path, right: Path) -> Path:
        self.asm = asm
        self.left = left
        self.right = right
        if (not left and right) or (left and not right):
            raise ValueError('must specify both left and right, or neither.')
        self.bks = set([asm])
        if left:
            self.bks |= left.bks
            self.bks |= right.bks

    def __eq__(self, other: Path) -> bool:
        return self.__hash__() == other.__hash__()

    def __hash__(self) -> int:
        return hash((self.asm,tuple(sorted(self.bks))))

    def __str__(self) -> str:
        if not self.left:
            return f'{self.Index()}:{self.asm}'
        return f'{self.Index()}:({self.left}|{self.right})'

    @cache
    def Index(self, exists: tuple[Assembly] = tuple()) -> int:
        if self.asm in exists:
            return 0

        l = self.left
        r = self.right
        if (not l and r) or (l and not r):
            raise ValueError('Invalid State: had only one of self.left and self.right set')
        if not l and not r:
            return 0  # this is an atom

        # assemble right from left's building blocks
        lidx = l.Index()
        ridx = r.Index(tuple(sorted(exists + tuple(l.bks))))
        lr_idx = ridx+lidx+1

        # assemble left from right's building blocks
        ridx = r.Index()
        lidx = l.Index(tuple(sorted(exists + tuple(r.bks))))
        rl_idx = ridx+lidx+1

        return min(lr_idx, rl_idx)

    @staticmethod
    def From(a: Assembly) -> Path:
        if not a.is_atom():
            raise ValueError("From() must be called with an Atom Assembly")
        return Path(a, None, None)

    # This algorithm assumes linear, ordered assemblies (aka strings)
    @staticmethod
    def Concat(left: Path,
               right: Path) -> Path:
        return Path(Assembly.Concat(left.asm,right.asm), left, right)

def MinStrPaths(s: str) -> list[Path]:
    layers: list[set[Path]] = list()
    atoms = set([Path.From(Assembly.Atom(c)) for c in s])
    layers.append(atoms)
    for l in tqdm(range(1,len(s)), "Generating Paths: "):
        next_layer = set()
        for i in range(int((l+1)/2)):
            l1 = layers[i]
            l2 = layers[l-i-1]
            next_layer |= set([
                Path.Concat(o1,o2)
                for o1 in l1 for o2 in l2 if str(o1.asm)+str(o2.asm) in s])
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

def generateAbracadabra() -> Path:
    # generate and return the Path that represents 'abracadabra'
    a = Path.From(Assembly.Atom('a')) # idx = 0
    b = Path.From(Assembly.Atom('b')) # idx = 0
    r = Path.From(Assembly.Atom('r')) # idx = 0
    c = Path.From(Assembly.Atom('c')) # idx = 0
    d = Path.From(Assembly.Atom('d')) # idx = 0
    ab = Path.Concat(a,b) # idx = 1
    abr = Path.Concat(ab,r) # idx = 2
    abra = Path.Concat(abr,a) # idx = 3
    abrac = Path.Concat(abra,c) # idx = 4
    abraca = Path.Concat(abrac,a) # idx = 5
    abracad = Path.Concat(abraca,d) # idx = 6
    abracadabra = Path.Concat(abracad,abra) # idx = 7
    print(abracadabra)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        assemble_str = 'abracadabra'
    else:
        assemble_str = sys.argv[1]
    print(f"print all min assembly paths for '{assemble_str}'")
    for path in MinStrPaths(assemble_str):
        print(path)


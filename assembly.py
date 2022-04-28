from __future__ import annotations

class Path:
    idx: int
    obj: str
    bks: set[Path]  # for caching only
    left: Path
    right: Path

    def __init__(self, obj: str, left: Path, right: Path) -> Path:
        self.obj = obj
        self.left = left
        self.right = right
        self.bks = set([obj])
        max_idx = 0
        if left:
            max_idx = max(max_idx, 1 + left.idx)
            self.bks |= left.bks
        if right:
            max_idx = max(max_idx, 1 + right.idx)
            self.bks |= right.bks
        self.idx = max_idx

    def __eq__(self, other: Path):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        lhash = 0 if not self.left else left.__hash__()
        rhash = 0 if not self.right else right.__hash__()
        hash((idx,obj,lhash,rhash))

    def __str__(self):
        return f'index of {self.idx}: {self.obj}'

    @staticmethod
    def Atom(s: str) -> Path:
        return Path(s, None, None)

    @staticmethod
    def From(left: Path, right: Path):
        return Path(f'({left.obj}|{right.obj})', left, right)

if __name__ == "__main__":
    # make the object that represents abracadabra
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

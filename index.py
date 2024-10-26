from typing import Iterator
from assembly import *
from sys import argv
import heapq
import math

class StrAsmIdxCache:
    target: Assembly
    hist: History
    score: int

    def __init__(self,
                 target: StringAssembly,
                 hist: History,
                 atoms: set[StringAssembly]):
        self.target = target
        self.hist = hist

        # do this once, instead of at every use
        target_str = str(target)
        hist_str = str(hist.asm)

        ############################################################
        ## score is a hard-coded heuristic to bring more likely
        ## history candidates to the top of the heap.
        ##
        ## In the future should be a learned heuristic.
        ############################################################

        # score is 0 if the history is not a substring of the target
        self.score = 1 if hist_str in target_str else 0
        if self.score == 0:
            return

        # bias towards smaller assembly indexes
        self.score *= len(hist_str) / math.log(hist.asm_idx + 2)

        # reverse the score since heapq is a min heap
        self.score *= -1

    def __lt__(self, other: 'StrAsmIdxCache') -> bool:
        return self.score < other.score
    
    def __str__(self) -> str:
        return f"Target: {self.target}\nScore: {self.score}\n{self.hist}"

def GenStrAsmIdx(s: str, debug: bool = False) -> Iterator[History]:
    target = StringAssembly.Create(s)
    hists = [History(AtomCtor(StrAtom(c))) for c in s]
    atoms = set([StrAtom(c) for c in s])

    # create a priority queue of StrAsmIdxCache objects
    pq = []
    for hist in hists:
        cache = StrAsmIdxCache(target, hist, atoms)
        heapq.heappush(pq, cache)

    best_hist = []
    best_asm_idx = len(s) + 1
    ctors = [StrAppendCtor, StrPrependCtor]

    cnt = 0
    while pq:
        cnt += 1
        if debug and cnt % 100 == 0:
            print(f"Queue size: {len(pq)}")

        cache = heapq.heappop(pq)
        for asm in (cache.hist.population | atoms):
            for ctor in ctors:
                ctor_hist = History(ctor(asm), parent=cache.hist)

                if ctor_hist.asm == target:
                    if ctor_hist.asm_idx < best_asm_idx:
                        best_hist = ctor_hist
                        best_asm_idx = ctor_hist.asm_idx
                        if debug:
                            print(f"New best:\n{best_hist}\n")
                        yield ctor_hist
                    # adding a history that is already the target is pointless
                    continue

                # add to heap to continue searching, if score isn't 0
                ctor_cache = StrAsmIdxCache(target, ctor_hist, atoms)
                if (ctor_cache.score != 0 and
                    ctor_cache.hist.asm_idx < best_asm_idx - 1):
                    heapq.heappush(pq, ctor_cache)

    if debug:
        print(f"Number of iterations: {cnt}")

    return best_hist


def main(s: str):
    for hist in GenStrAsmIdx(s):  #, debug=True):
        print(f"New Best:\n{hist}\n")

if __name__ == "__main__":
    main(argv[1] if len(argv) > 1 else 'abracadabra')

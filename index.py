from typing import Iterator
from assembly import *
from itertools import product
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
                 parent: 'StrAsmIdxCache' = None,
                 check_sub: bool = True):
        self.target = target
        self.hist = hist
        self.parent = parent

        ############################################################
        ## score is a hard-coded heuristic to bring more likely
        ## history candidates to the top of the heap.
        ##
        ## In the future this should be a learned heuristic.
        ############################################################
        self.score = 1

        # do this once, instead of at every use
        target_str = str(target)
        hist_str = str(hist.asm)
        
        # score is 0 if the history is not a substring of the target
        if check_sub and hist_str not in target_str:
            self.score = 0
            return
        
        # find minimum number of steps left to reach the target
        self.min_steps_left = self.parent.min_steps_left if self.parent else len(target_str)
        self.breadth_left = len(target.el_cnts) - len(hist.asm.el_cnts)
        self.depth_left = 0
        for el, cnt in target.el_cnts.items():
            hist_cnt = hist.asm.el_cnts.get(el, 1)
            self.depth_left = max(self.depth_left, math.ceil(math.log(cnt / hist_cnt, 2)))
        self.min_steps_left = min(self.min_steps_left, self.breadth_left + self.depth_left)

        # include scores from parent scores
        self.score *= (-self.parent.score) if self.parent else 1

        # bias towards fewer steps left to reach the target
        self.score *= len(target_str) / (self.min_steps_left + 1)

        # bias towards lower assembly indexes
        self.score *= (len(hist_str) / (hist.asm_idx + 1))**2

        # bias towards assemblies that have smaller strings after
        # it's population matches the remainder of the target string.
        splits = [sp for sp in target_str.split(hist_str) if sp]
        for asm in hist.population:
            str_asm = str(asm)
            if len(str_asm) == 1:
                continue
            num_repl = 1
            for split in splits:
                if str_asm in split:
                    num_repl += (len(split) - len(split.replace(str_asm, ''))) / len(split)
            self.score *= 1 + 0.001 * (num_repl**2 * (len(str_asm) - 1)**2 / (sum(len(s) for s in splits) + 1))

        # reverse the score since heapq is a min heap
        self.score *= -1

    def __lt__(self, other: 'StrAsmIdxCache') -> bool:
        return self.score < other.score
    
    def __str__(self) -> str:
        return f"Target: {self.target}\nScore: {self.score}\n{self.hist}"

def GenStrAsmIdx(s: str, debug: bool = False) -> Iterator[History]:
    target = StringAssembly.Create(s)
    atoms = set([StrAtom(c) for c in s])
    hists = [History(AsmCtor(atom), population=atoms) for atom in atoms]

    # create a priority queue of StrAsmIdxCache objects
    pq = []
    for hist in hists:
        cache = StrAsmIdxCache(target, hist, parent=None)
        heapq.heappush(pq, cache)

    best_hist = []
    best_asm_idx = len(s) + 1
    ctors = [StrAppendAsmCtor]

    cnt = 0
    while pq:
        cnt += 1
        if debug and cnt % 100 == 0:
            print(f"Queue size: {len(pq)}")

        cache = heapq.heappop(pq)
        for asm1, asm2 in product(cache.hist.population, repeat=2):
            for ctor in ctors:
                ctor_asm = ctor(asm1, asm2)
                if ctor_asm() in cache.hist.population:
                    continue
                ctor_hist = History(ctor_asm, parent=cache.hist)

                # check if the new assembly is the target
                if ctor_hist.asm == target:
                    if ctor_hist.asm_idx < best_asm_idx:
                        best_hist = ctor_hist
                        best_asm_idx = ctor_hist.asm_idx
                        if debug:
                            print(f"New best:\n{best_hist}\n")
                        yield best_hist
                    continue  # skip adding to heap

                # add to heap to continue searching, if score isn't 0
                ctor_cache = StrAsmIdxCache(target, ctor_hist, parent=cache)
                if (ctor_cache.score != 0 and
                    ctor_cache.hist.asm_idx + ctor_cache.min_steps_left < best_asm_idx):
                    heapq.heappush(pq, ctor_cache)

    if debug:
        print(f"Number of iterations: {cnt}")

    return best_hist


def main(s: str):
    for hist in GenStrAsmIdx(s):  #, debug=True):  # if you want to monitor heap size
        print(f"New Best:\n{hist}\n")

if __name__ == "__main__":
    main(argv[1] if len(argv) > 1 else 'abracadabra')

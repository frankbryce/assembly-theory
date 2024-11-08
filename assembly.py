from __future__ import annotations

import networkx as nx
from typing import Callable, List

class Assembly:
    graph: nx.Graph
    atoms: list[tuple[int, dict[str, str]]]
    _global_atom_id: int = 1  # Global variable to track unique atom IDs across all assemblies

    @classmethod
    def Atom(cls, element: str):
        ret = cls()
        ret.graph = nx.Graph()
        ret.atoms = [(Assembly._global_atom_id, {'element': element})]
        ret.graph.add_nodes_from(ret.atoms)
        ret.el_cnts = {element: 1}
        Assembly._global_atom_id += 1
        return ret

    @classmethod
    def Join(cls, asms: list[Assembly], edges: list[tuple[int, int]]) -> Assembly:
        if len(asms) == 0:
            raise ValueError("Cannot join an empty list of assemblies")
        
        asm_type = asms[0].__class__
        for asm in asms[1:]:
            if asm.__class__ != asm_type:
                raise ValueError("All assemblies must be of the same type")

        # initialize the return assembly
        ret = cls()

        # copy the assemblies and map the atoms
        edge_map = dict()
        cloned_asms = list()
        for asm in asms:
            cloned_asm, new_map = cls.CopyAndMap(asm)
            for k,v in new_map.items():
                edge_map[k] = v
            cloned_asms.append(cloned_asm)
        asms = cloned_asms

        # compose the assembly graphs
        last_asm = asms[0]
        ret.atoms = last_asm.atoms
        ret.el_cnts = {**last_asm.el_cnts}
        for asm in asms[1:]:
            ret.graph = nx.compose(last_asm.graph, asm.graph)
            ret.atoms += asm.atoms
            last_asm = asm
            for el, cnt in asm.el_cnts.items():
                ret.el_cnts[el] = ret.el_cnts.get(el, 0) + cnt

        # add the new edges based on the node mapping done earlier
        for edge in edges:
            edge = (edge_map[edge[0]], edge_map[edge[1]])
            ret.graph.add_edge(edge[0], edge[1])

        return ret

    def is_atom(self) -> bool:
        return len(self.atoms) == 1

    def __lt__(self, other: Assembly) -> bool:
        return self.__hash__() < other.__hash__()

    def __eq__(self, other: Assembly) -> bool:
        return self.__hash__() == other.__hash__()
        
    def __hash__(self):
        return int(nx.weisfeiler_lehman_graph_hash(self.graph, node_attr='element'))

    def __str__(self) -> str:
        return str(self.graph.nodes(data=True))
    
    def __len__(self) -> int:
        return len(self.atoms)


    @classmethod
    def Copy(cls, asm: Assembly) -> Assembly:
        return cls.CopyAndMap(asm)[0]

    @classmethod
    def CopyAndMap(cls, asm: Assembly) -> tuple[Assembly, dict[int, int]]:
        ret = cls()
        ret.atoms = list()
        ret.el_cnts = {**asm.el_cnts}
        old_to_new = dict()
        for atom in asm.atoms:
            cloned = cls.Atom(atom[1]['element'])
            old_to_new[atom[0]] = cloned.atoms[0][0]
            ret.atoms.append(cloned.atoms[0])
        ret.graph = nx.relabel_nodes(asm.graph, old_to_new)
        return ret, old_to_new

class StringAssembly(Assembly):

    @staticmethod
    def Create(s: str) -> StringAssembly:
        assembly = None
        for c in s:
            atom = StringAssembly.Atom(c)
            if assembly:
                assembly = assembly.Append(atom)
            else:
                assembly = atom
        return assembly

    def Append(self, right: StringAssembly) -> StringAssembly:
        left = self
        return self.__class__.Join([left, right],
                                   [(left.atoms[-1][0], right.atoms[0][0])])

    def __lt__(self, other: StringAssembly) -> bool:
        return self.__hash__() < other.__hash__()

    def __eq__(self, other: StringAssembly) -> bool:
        return self.__hash__() == other.__hash__()
        
    def __hash__(self):
        return self.__str__().__hash__()

    def __str__(self) -> str:
        return ''.join([a['element'] for _,a in sorted(self.graph.nodes(data=True), key=lambda n: n[0])])


class Constructor:
    asms: list[Assembly]

    def __init__(self, *asms: Assembly) -> None:
        for asm in asms:
            if (not issubclass(asm.__class__, Assembly) and
                not issubclass(asm.__class__, History)):
                raise ValueError("All assemblies must be of type Assembly or History")

        self.asms = [asm if not issubclass(asm.__class__, History) else asm.asm
                     for asm in asms]

    def __call__(self, _: Assembly | None = None) -> Assembly:
        raise NotImplementedError("Subclasses must implement this method")

class AsmCtor(Constructor):
    def __call__(self, _: Assembly | None = None) -> Assembly:
        if len(self.asms) != 1:
            raise ValueError("AsmCtor expects exactly one assembly")
        return self.asms[0]

class StrAppendAsmCtor(Constructor):
    def __call__(self, _: Assembly | None = None) -> Assembly:
        if len(self.asms) != 2:
            raise ValueError("StrAppendAsmCtor expects exactly two assemblies")
        return self.asms[0].Append(self.asms[1])

class StrAppendCtor(Constructor):
    def __call__(self, p: Assembly | None = None) -> Assembly:
        if p is None:
            raise ValueError("StrAppendCtor expects an assembly as input")
        if len(self.asms) != 1:
            raise ValueError("StrAppendCtor expects exactly one assembly")
        return p.Append(self.asms[0])
    
class StrPrependCtor(Constructor):
    def __call__(self, p: Assembly | None = None) -> Assembly:
        if p is None:
            raise ValueError("StrPrependCtor expects an assembly as input")
        if len(self.asms) != 1:
            raise ValueError("StrPrependCtor expects exactly one assembly")
        return self.asms[0].Append(p)


class History:
    asm_idx: int
    asm: Assembly
    population: set[Assembly]
    parent: History
    constructor: Constructor

    def __init__(self,
                 constructor: Constructor,
                 parent: History | None = None,
                 population: set[Assembly] = set()) -> None:
        self.constructor = constructor
        self.parent = parent
        self.population = parent.population.copy() if parent else population.copy()

        for asm in constructor.asms:
            if asm.is_atom():
                continue
            if asm not in self.population:
                raise ValueError("All assemblies must be atoms or from the history's population")

        self.asm = constructor(parent.asm if parent else None)
        self.asm_idx = parent.asm_idx + 1 if parent else 0
        self.population.add(self.asm)

    def __str__(self) -> str:
        if self.parent:
            ret = f"{self.parent}\n"
            ret += f"H[{self.asm_idx}]: {self.asm}, ("
            ret += f"{', '.join([str(asm) for asm in self.constructor.asms])}"
            ret += ")"
            return ret
        else:
            return f"H[{self.asm_idx}]: {self.asm}"

    def __hash__(self):
        ret = self.asm.__hash__()
        ret <<= 17  # some arbitrary number
        for asm in self.population:
            ret ^= asm.__hash__()
        ret <<= self.asm_idx
        return ret

# type aliases
StrAtom = StringAssembly.Atom

if __name__ == "__main__":
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
    print(abracadabra)

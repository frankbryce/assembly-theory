from __future__ import annotations

import networkx as nx
from typing import Callable, List

class Assembly:
    graph: nx.Graph
    atoms: list[tuple[int, dict[str, str]]]
    _global_atom_id: int = 1  # Global variable to track unique atom IDs across all assemblies
    _global_atom_map: dict[int, nx.Graph] = dict()

    @classmethod
    def Atom(cls, element: str):
        ret = cls()
        ret.graph = nx.Graph()
        ret.graph.add_nodes_from([(Assembly._global_atom_id, {'element': element})])
        ret.atoms = [(node, data) for node, data in ret.graph.nodes(data=True)]
        Assembly._global_atom_map[Assembly._global_atom_id] = ret.atoms
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
        ret = cls()
        ret.atoms = last_asm.atoms
        for asm in asms[1:]:
            ret.graph = nx.compose(last_asm.graph, asm.graph)
            ret.atoms += asm.atoms
            last_asm = asm

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
        return int(nx.weisfeiler_lehman_graph_hash(self.graph, node_attr='element'), 16)

    def __str__(self) -> str:
        return str(self.graph.nodes(data=True))


    @classmethod
    def Copy(cls, asm: Assembly) -> Assembly:
        return cls.CopyAndMap(asm)[0]

    @classmethod
    def CopyAndMap(cls, asm: Assembly) -> tuple[Assembly, dict[int, int]]:
        ret = cls()
        ret.atoms = list()
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
                assembly = StringAssembly.Concat(assembly, atom)
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


class History:
    asm_idx: int
    asm: Assembly
    ctor_asms: list[Assembly]  
    population: set[Assembly]
    parent: History
    constructor: Callable[[History | None, List[Assembly] | None], Assembly]

    def __init__(self,
                 constructor: Callable[[History | None, List[Assembly] | None], Assembly],
                 *ctor_asms: list[Assembly | History],
                 parent: History | None = None) -> None:
        self.constructor = constructor
        self.parent = parent

        self.population = set()
        if parent:
            self.population.update(parent.population)

        for asm in ctor_asms:
            if (not issubclass(asm.__class__, Assembly) and
                not issubclass(asm.__class__, History)):
                raise ValueError("All assemblies must be of type Assembly or History")
            if issubclass(asm.__class__, History):
                asm = asm.asm
            if asm.is_atom():
                continue
            if asm not in self.population:
                raise ValueError("All assemblies must be atoms or from the history's population")

        self.asm = constructor(parent,
                               [asm if not issubclass(asm.__class__, History) else asm.asm
                                for asm in ctor_asms])
        self.ctor_asms = ctor_asms
        self.asm_idx = parent.asm_idx + 1 if parent else 0
        self.population.add(self.asm)

    def __str__(self) -> str:
        if self.parent:
            ret = f"H[{self.asm_idx}]: {self.asm}, ("
            ret += f"{', '.join([str(asm) if not issubclass(asm.__class__, History) else str(asm.asm) for asm in self.ctor_asms])}"
            ret += ")\n"
            ret += f"{self.parent}"
            return ret
        else:
            return f"H[{self.asm_idx}]: {self.asm}"

# Pre-made constructors for convenience
def AtomCtor(_, asms: list[Assembly]) -> Assembly:
    if len(asms) != 1:
        raise ValueError("AtomCtor expects exactly one assembly")
    return asms[0]

def StrAppendCtor(p: History, asms: list[Assembly]) -> Assembly:
    if len(asms) != 1:
        raise ValueError("StrAppendCtor expects exactly one assembly")
    return p.asm.Append(asms[0])

# type aliases
StrAtom = StringAssembly.Atom

if __name__ == "__main__":
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
    print(abracadabra)

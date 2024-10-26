# Assembly Theory (Open Source Code)

Contains code for modeling, and finding the optimal history of, assemblies in order to determine their assembly index as defined by https://en.wikipedia.org/wiki/Assembly_theory.

## Overview of Code Structure

![AssemblyTheoryDepOverview](https://raw.githubusercontent.com/frankbryce/assembly-theory/refs/heads/main/AssemblyTheoryDepOverview.png)

* `Assembly` objects allow you to specify atoms, and also the ability to join assemblies together. The underlying datatype for this is a `networkx.Graph` object, but the `Assembly` object provides niceties like `__hash__` and `Join`. This is the base dependency for all other parts of the codebase.
  * Currently, the only useful Assembly is a `StringAssembly`, but I'd like to add molecular assemblies as well. `StringAssembly` is a subclass of `Assembly` which is useful to encode the idea of joining strings. `networkx.Graph` objects have more degrees of freedom when composing graphs together. String assemblies look like `node - node - node ... - node`.
  * Atom assemblies are single element graphs, and can be created with `Assembly.Atom()` or `StringAssembly.Atom()` for string assemblies.
* `Constructor` objects allow you to specify how to turn assemblies into other assemblies. You can accept assemblies to hold in the object and use them during construction.
* `History` objects hold information about the lineage of an assembly. To make a `History` object, you need to pass in a set of assemblies, an (optional) parent, and a constructor.
  * If a parent is not specified, all assemblies must be atoms. If you attempt to use a constructor that has non-atom assemblies it will raise an error.
  * The `History` keep a memory of all assemblies created in this History chain of construction. This is called the `population` of assemblies for this history.
  * If you attempt to use a constructor with assemblies not in the current `population` it will raise an error.
  * `History` will call the specified constructor with the parent assembly (or `None` if no parent is provided). It will return the assembly that will be associated with this `History` object.
  * `History` tracks the assembly index of this history, by adding 1 each time, or starting at `0` if this is an atom history with no parent.
* `AtomCtor`, `StrAppendCtor`, and `StrPrependCtor` are pre-made Constructors for convenience. As more `Assembly` types are added, more constructors will also be added.
* In `index.py`, `GenStrAsmIdx` is a generator which yields subsequently improved histories, as measured by the assembly index. It uses a `heapq` priority queue to search through the space of `History` objects for a target string. There is room for improvement here, as it can be quite slow for long strings. Being able to more efficiently discard Histories is a big opportunity for improvement.

## `assembly.py`

This file contains the basic definitions of `Assembly`, `Constructor`, and `History` objects.

I have a few tests written, which can be run with the following command:

```bash
$ python -m unittest assembly_test.py
```

Here is some example code you can after importing `assembly.py`. This is what `assembly.py` does if you execute it
directly. The `History` object holds information necessary to remember the lineage of an assembly. A given assembly may be
constructed by many different `History`s.

```py
# AtomCtor is a basic constructor for a single atom.
# StrAtom is an alias for StringAssembly.Atom
a = History(AtomCtor(StrAtom('a')))
b = History(AtomCtor(StrAtom('b')))
r = History(AtomCtor(StrAtom('r')))
c = History(AtomCtor(StrAtom('c')))
d = History(AtomCtor(StrAtom('d')))

# StrAppendCtor is a constructor for appending an atom to a history's assembly.
# If the assembly passed in is not in the parent History, it will raise an error..
ab = History(StrAppendCtor(b), parent=a)
abr = History(StrAppendCtor(r), parent=ab)
abra = History(StrAppendCtor(a), parent=abr)
abrac = History(StrAppendCtor(c), parent=abra)
abraca = History(StrAppendCtor(a), parent=abrac)
abracad = History(StrAppendCtor(d), parent=abraca)
abracadabra = History(StrAppendCtor(abra), parent=abracad)
print(abracadabra)
```

Currently, the output of `assembly.py` is a history of the example string from the wikipedia article, `"abracadabra"`.

<details>
<summary>`assembly.py` example output</summary>

```bash
$ python3 assembly.py
H[0]: a
H[1]: ab, (b)
H[2]: abr, (r)
H[3]: abra, (a)
H[4]: abrac, (c)
H[5]: abraca, (a)
H[6]: abracad, (d)
H[7]: abracadabra, (abra)
```

</details>

## `index.py`

This file contains an algorithm for finding the minimum `History` to construct a string using string concatenation. It's slow for long strings, so the tests take a while to run (3-4 minutes on my machine). They can be run with the following command:

```bash
$ python -m unittest index_test.py
```

Here is code you can run after importing `index.py` to see the output. This is what
`index.py` runs if you execute it directly.

```py
# This will yield History objects as new best histories are found for lowering
# the assembly index. There are other objects in this file, but are meant for
# internal use. GenStrAsmIdx = "generator of string assembly indices".
for hist in GenStrAsmIdx(s):  #, debug=True):  # if you want to see the debug output
    print(f"New Best:\n{hist}\n")
```

Currently, the output of `index.py` is generator outputting the next
best history to construct the target string. You can pass in a target
string or `abracadabra` is set as the default.

<details>
<summary>`index.py` example output</summary>

```bash
$ python3 index.py
New Best:
H[0]: a
H[1]: ac, (c)
H[2]: rac, (r)
H[3]: brac, (b)
H[4]: braca, (a)
H[5]: bracad, (d)
H[6]: bracada, (a)
H[7]: bracadab, (b)
H[8]: bracadabr, (r)
H[9]: bracadabra, (a)
H[10]: abracadabra, (a)

New Best:
H[0]: a
H[1]: ra, (r)
H[2]: rac, (c)
H[3]: raca, (a)
H[4]: racad, (d)
H[5]: racada, (a)
H[6]: racadab, (b)
H[7]: racadabra, (ra)
H[8]: bracadabra, (b)
H[9]: abracadabra, (a)

New Best:
H[0]: a
H[1]: ra, (r)
H[2]: bra, (b)
H[3]: brac, (c)
H[4]: braca, (a)
H[5]: abraca, (a)
H[6]: abracad, (d)
H[7]: abracada, (a)
H[8]: abracadabra, (bra)

New Best:
H[0]: a
H[1]: ra, (r)
H[2]: bra, (b)
H[3]: abra, (a)
H[4]: abrac, (c)
H[5]: abraca, (a)
H[6]: abracad, (d)
H[7]: abracadabra, (abra)
```

</details>

## Dependencies

You can install them with pip:

```bash
$ python3 -m pip install -r requirements.txt
```

# Assembly Theory (Open Source Code)

Working on algorithm to find complexity of arbitrary assemblies, modeled by networkx.Graph objects, as defined by https://en.wikipedia.org/wiki/Assembly_theory

The current version of this models the differences between assemblies and string assemblies, and separates out the assembled object from its history, and abstracts the idea of construction to a lambda which can take parent assemblies as arguments.

## `assembly.py`

This file contains the basic definitions of the Assembly History objects, as well as a few constructors for string assemblies for
convenience.

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
a = History(AtomCtor, StrAtom('a'))
b = History(AtomCtor, StrAtom('b'))
r = History(AtomCtor, StrAtom('r'))
c = History(AtomCtor, StrAtom('c'))
d = History(AtomCtor, StrAtom('d'))

# StrAppendCtor is a constructor for appending an atom to a history's assembly.
# if the assembly passed in is not in the parent assembly, it will raise an error..
ab = History(StrAppendCtor, b, parent=a)
abr = History(StrAppendCtor, r, parent=ab)
abra = History(StrAppendCtor, a, parent=abr)
abrac = History(StrAppendCtor, c, parent=abra)
abraca = History(StrAppendCtor, a, parent=abrac)
abracad = History(StrAppendCtor, d, parent=abraca)
abracadabra = History(StrAppendCtor, abra, parent=abracad)
print(abracadabra)
```

Currently, the output of assembly.py is a basic history of the example string from the wikipedia article.

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

This file contains the main algorithm for finding the minimum history to construct a string using string concatenation. It's
quite slow for long strings, so the tests take a while to run (several minutes). They can be run with the following command:

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

Currently, the output of `index.py` is generator outputing the next
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

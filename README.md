# assembly-theory
Working on algorithm to find complexity of arbitrary assemblies, modeled by networkx.Graph objects, as defined by https://en.wikipedia.org/wiki/Assembly_theory

The current version of this models the differences between assemblies and string assemblies, and separates out the assembled object from its history, and abstracts the idea of construction to a lambda which can take parent assemblies as arguments.

I have a few basic tests written, which can be run with the following command:

```bash
$ python -m unittest assembly_test.p
```

Currently, the output of assembly.py is a basic history of the example string from the wikipedia article.

```bash
$ python3 assembly.py
H[7]: abracadabra, (abra)
H[6]: abracad, (d)
H[5]: abraca, (a)
H[4]: abrac, (c)
H[3]: abra, (a)
H[2]: abr, (r)
H[1]: ab, (b)
H[0]: a
```

## Dependencies

You can install them with pip:

```bash
$ python3 -m pip install -r requirements.txt
```


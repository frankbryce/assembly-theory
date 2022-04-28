# assembly-theory
Working on algorithm to find complexity of strings by https://en.wikipedia.org/wiki/Assembly_theory

Using this algorithm, I discovered there are many assembly paths for abracadabra of index 7.

```bash
$ python3 assembly.py 
print all min assembly paths for 'abracadabra'
index of 7: (((a|b)|(r|a))|((c|a)|(d|((a|b)|(r|a)))))
index of 7: ((a|(b|(r|a)))|(c|((a|d)|(a|(b|(r|a))))))
index of 7: (((a|b)|(r|a))|(c|(a|(d|((a|b)|(r|a))))))
index of 7: (((a|b)|(r|a))|(c|((a|d)|((a|b)|(r|a)))))
index of 7: ((a|(b|(r|a)))|(c|(a|(d|(a|(b|(r|a)))))))
index of 7: (((a|b)|(r|a))|((c|(a|d))|((a|b)|(r|a))))
index of 7: ((a|(b|(r|a)))|((c|(a|d))|(a|(b|(r|a)))))
index of 7: ((a|(b|(r|a)))|((c|a)|(d|(a|(b|(r|a))))))
```

## Dependencies

This isn't a super involved repo (yet), but I do put the modest dependencies in a requirements.txt file

```bash
$ python3 -m pip install -r requirements.txt
```

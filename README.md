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

$ python3 assembly.py sdflkjsdflkjsdflkj
print all min assembly paths for 'sdflkjsdflkjsdflkj'
Generating Paths: 100%|████████████████████████████████████████████████████████████████████████| 17/17 [00:06<00:00,  2.65it/s]
Looking for min index: 100%|████████████████████████████████████████████████████████████| 60958/60958 [02:42<00:00, 375.49it/s]
index of 8: ((s|(d|(f|(l|(k|j)))))|((s|(d|(f|(l|(k|j)))))|(s|(d|(f|(l|(k|j)))))))
index of 8: ((s|((d|f)|(l|(k|j))))|((s|((d|f)|(l|(k|j))))|(s|((d|f)|(l|(k|j))))))
index of 8: ((s|(d|((f|l)|(k|j))))|((s|(d|((f|l)|(k|j))))|(s|(d|((f|l)|(k|j))))))
```

## Dependencies

This isn't a super involved repo (yet), but I do put the modest dependencies in a requirements.txt file

```bash
$ python3 -m pip install -r requirements.txt
```

# assembly-theory
Working on algorithm to find complexity of strings by https://en.wikipedia.org/wiki/Assembly_theory

Using this algorithm, I discovered there are many assembly paths for abracadabra of index 7.

Feel free to pass in strings of your own, or send pull requests! Example outputs below.

```bash
$ python3 assembly.py
print all min assembly paths for 'abracadabra'
Generating Paths: 100%|█████████████████████████████████████████████████████████| 10/10 [00:00<00:00, 114.11it/s]
Looking for min index: 100%|████████████████████████████████████████████████| 210/210 [00:00<00:00, 23278.90it/s]
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(0:c|5:(0:a|4:(0:d|3:(0:a|2:(0:b|1:(0:r|0:a)))))))
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(2:(0:c|1:(0:a|0:d))|3:(0:a|2:(0:b|1:(0:r|0:a)))))
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(1:(0:c|0:a)|4:(0:d|3:(0:a|2:(0:b|1:(0:r|0:a))))))
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(0:c|5:(1:(0:a|0:d)|3:(0:a|2:(0:b|1:(0:r|0:a))))))
7:(3:(0:a|2:(0:b|1:(0:r|0:a)))|6:(2:(0:c|1:(0:a|0:d))|3:(0:a|2:(0:b|1:(0:r|0:a)))))
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(0:c|5:(0:a|4:(0:d|3:(1:(0:a|0:b)|1:(0:r|0:a))))))
7:(3:(0:a|2:(0:b|1:(0:r|0:a)))|6:(1:(0:c|0:a)|4:(0:d|3:(0:a|2:(0:b|1:(0:r|0:a))))))
7:(3:(0:a|2:(0:b|1:(0:r|0:a)))|6:(0:c|5:(0:a|4:(0:d|3:(0:a|2:(0:b|1:(0:r|0:a)))))))
7:(3:(0:a|2:(0:b|1:(0:r|0:a)))|6:(0:c|5:(1:(0:a|0:d)|3:(0:a|2:(0:b|1:(0:r|0:a))))))
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(1:(0:c|0:a)|4:(0:d|3:(1:(0:a|0:b)|1:(0:r|0:a)))))
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(2:(0:c|1:(0:a|0:d))|3:(1:(0:a|0:b)|1:(0:r|0:a))))
7:(3:(1:(0:a|0:b)|1:(0:r|0:a))|6:(0:c|5:(1:(0:a|0:d)|3:(1:(0:a|0:b)|1:(0:r|0:a)))))

$ python3 assembly.py sdfsdf
print all min assembly paths for 'sdfsdf'
Generating Paths: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 4778.20it/s]
Looking for min index: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 6/6 [00:00<00:00, 35696.20it/s]
3:(2:(0:s|1:(0:d|0:f))|2:(0:s|1:(0:d|0:f)))
```

## Dependencies

This isn't a super involved repo (yet), but I do put the modest dependencies in a requirements.txt file

```bash
$ python3 -m pip install -r requirements.txt
```


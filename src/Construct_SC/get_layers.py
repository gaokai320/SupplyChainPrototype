from collections import defaultdict
import sys

sc_name = sys.argv[1]
first_layer = sys.argv[2]
proj2down = defaultdict(list)

with open(sc_name) as f:
    for line in f:
        proj, ups = line.strip('\n').split(';')
        for u in ups.split(','):
            proj2down[u].append(proj)

proj2layers = defaultdict(list)
proj2layers[first_layer].append(1)
packages = set(proj2down.keys())
next_layer = set(proj2down[first_layer])
layer = 2
while next_layer:
    print("constructing layer %s" % layer)
    for down in next_layer:
        proj2layers[down].append(layer)
    layer = layer + 1
    cur_packages = packages.intersection(next_layer)
    next_layer = []
    for p in cur_packages:
        next_layer.extend(proj2down[p])
    next_layer = set(next_layer)

with open('data/' + first_layer + '.layer', 'w') as f:
    for k, v in proj2layers.items():
        f.write(k + ':' + ','.join(list(map(str, v))) + '\n')

summary = defaultdict(int)
for k, v in proj2layers.items():
    summary[','.join(list(map(str, v)))] += 1
print(summary)%
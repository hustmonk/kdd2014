#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

def find(idx_num, v, start, end):
    if start >= end:
        return start
    mid = (start + end) / 2
    if (idx_num[mid] == v):
        return mid
    elif idx_num[mid] > v:
        return find(idx_num, v, start, mid - 1)
    else:
        return find(idx_num, v, mid + 1, end)

def idf(arr):
    N = 50
    vset = set(arr)
    kids = []
    print len(vset)
    if len(vset) < N:
        for k in arr:
            kids.append(str(k))
        return [], kids

    sort = sorted([k for k in arr if k > 0.00001])
    idx_num = []
    for i in range(N):
        idx = int(i * len(sort)/N)
        idx_num.append(sort[idx])
    ks = sum(idx_num[1:N-1]) / N
    print idx_num
    print ks

    old_feature = []
    for v in arr:
        if v < 0.00001:
            idx = 0
        else:
            idx = find(idx_num, v, 0, N) + 1
        kids.append(str(idx))
        
        if ks > 0:
            v = float(v) / ks
        old_feature.append(v)
    return old_feature,kids

def expand(features):
    expand_set = [[] for i in range(len(features))]
    print len(features)
    N = 100
    feature_ids = []
    for i in range(len(features[0])):
        if features[0][i][0:4] == 'True' or "False" == features[0][i][0:5] or features[0][i].find(":") > 0 or features[0][i][0] == 'R':
            continue
        value_set = set()
        for k in features:
            value_set.add(k[i])
        if len(value_set) < N:
            feature_ids.append(i)
            for j in range(len(features)):
                expand_set[j].append(features[j][i])
        if len(expand_set[0]) > 8:
            break

    print feature_ids
    if len(expand_set[0]) < 2:
        return
    for w in range(len(features)):
        for i in range(len(expand_set[0])):
            for j in range(i+1, len(expand_set[0])):
                features[w].append(expand_set[w][i]+"Q"+expand_set[w][j])
    return

def before(dat):
    if dat.find("-") < 0:
        return True
    year,month,day = dat.split("-")
    if int(year) < 2010:
        return True
    if int(year) == 2010 and int(month) < 4:
        return True
    return False

def labelToY(arr):
    total = 0
    if arr[0] == 't':
        total = 100
    for k in arr[1:]:
        if k == 't':
            total += 1
    return total


if __name__ == '__main__':
    p = range(1,200)
    idf("p",p)

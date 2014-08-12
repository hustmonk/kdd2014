#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import csv

__revision__ = '0.1'
file_list = ["sub.csv", "sub.csv.merge.top", "sub.csv.user"]
merge = {}
for filename in file_list:
    pids = []
    weight = 0.2
    if filename == 'sub.csv.merge.top':
        weight = 1
    reader = csv.reader(file(filename, 'rb'))
    reader.next()
    for line in reader:
        pid,score = line
        merge[pid] = merge.get(pid, 0) + float(score) * weight
        pids.append(pid)

fout = open("sub.merge.csv", 'w')
fout.write("projectid,is_exciting\n")
for pid in pids:
    fout.write("%s,%f\n" % (pid, merge[pid]))


#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
vp = {}
xdate = {}
for line in open("../data/projects.csv"):
    arr = line.strip().split(",")
    pid = arr[0]
    date = arr[-1]
    if date[0:4] == '2014':
        xdate[pid] = date
sort = sorted(xdate.items(), key=lambda x:x[1])
pid_weight = {}

for (pid,date) in sort:
    pid_weight[pid] = 1 - (len(pid_weight)/(0.1+len(sort))) * 0.8
for line in open("sub.csv.61669"):
    id,pre = line.strip().split(",")
    if pre == "is_exciting":
        continue
    vp[id] = str(float(pre) * pid_weight[id])
fin = open('../data/sampleSubmission.csv')
print fin.next().strip()

for line in fin:
    qid = line.split(",")[0]
    if qid in vp:
        #print "%s,%s,%s" % (qid, vp[qid], xdate[qid])
        print "%s,%s" % (qid, vp[qid])

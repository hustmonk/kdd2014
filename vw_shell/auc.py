#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from sklearn.metrics import roc_curve, auc
import sys
y_test = []
probas_ = []
pids = []
workspace=sys.argv[1]
for line in open(workspace+"train.txt2"):
    line = line.split(" ")
    if int(line[0]) < 19:
        y_test.append(0)
    else:
        y_test.append(1)
    pids.append(line[1].strip())
#for line in open("../result_data/rotten.trainpreds.txt"):
for line in open(workspace+"rotten.rawpreds.txt"):
    probas_.append(float(line.strip().split(" ")[0]))
#for i in range(len(y_test)):
#    print "%d\t%f\t%s" % (y_test[i], probas_[i], pids[i])
fpr, tpr, thresholds = roc_curve(y_test, probas_)
roc_auc = auc(fpr, tpr)
fout = open(workspace+"bak.auc","a")
fout.write("%f\n" % roc_auc)
print roc_auc

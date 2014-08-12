#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
from scipy import sparse

__revision__ = '0.1'

def read_file(file_name):
    feature_idx = {}
    for line in open("feature.list"):
        arr = line.strip().split(" ")
        feature_idx[arr[0]] = len(feature_idx)

    feature_i = []
    feature_j = []
    feature_v = []
    line_idx = 0
    Y = []
    for line in open(file_name):
        namespaces = line.strip().split("|")
        Y.append(float(namespaces[0].split(" ")[0]))
        for namespace in namespaces[1:]:
            arr = namespace.split(" ")
            space_name = arr[0]
            for kv in arr[1:]:
                key = kv
                value = "1"
                if key.find(":")>0:
                    key,value = key.split(":")
                key = space_name + "^" + key
                if key not in feature_idx:
                    continue
                feature_i.append(line_idx)
                feature_j.append(feature_idx[key])
                feature_v.append(float(value))
        line_idx = line_idx + 1
    print len(feature_v)
    return sparse.coo_matrix((feature_v, (feature_i, feature_j)), shape=(line_idx, len(feature_idx))), Y

X,Y = read_file("train.txt1")
test_X,test_Y = read_file("train.txt2")
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
clf = linear_model.LinearRegression()
clf = RandomForestRegressor(n_estimators = 30)
clf = GradientBoostingRegressor()
clf = linear_model.Ridge (alpha = .5)
clf = linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
clf.fit(X,Y)
preds = clf.predict(test_X)
fout = open("rotten.rawpreds.txt", "w")
for k in preds:
    fout.write("%f\n" % k)

#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import csv
from common import *

__revision__ = '0.1'
class Project:
    def __init__(self):
        self.type_dict = {}
        for line in open("type.dict"):
            if line[0] == '#':
                continue
            arr = line.strip().split("\t")
            self.type_dict[arr[2]] = arr[3]
        self.read_file()

    def out_features(self, kv):
        features = []
        for (k, v) in kv.items():
            if k not in self.type_dict:
                continue
            if k == "date_posted":
                v = v[5:7]
            if self.type_dict[k] == 'idf':
                features.append("%s:%.2f" % (k, float(v)/1000))
            elif self.type_dict[k] == 'id':
                features.append(k+"_"+v.replace(" ", ""))
            elif self.type_dict[k] == 'english':
                features.append(v)
        return (" ".join(features))

    def read_file(self):
        data_dir = '../data/'
        reader = csv.reader(file(data_dir + "projects.csv", 'rb'))
        header = reader.next()
        project_idx = 0
        self.resources_feature = {}
        for i in range(len(header)):
            if header[i] == 'projectid':
                project_idx = i
                break

        for line in reader:
            projectid = line[project_idx]
            if  before(line[-1]):
                continue
            kv = {}
            for i in range(len(header)):
                kv[header[i]] = line[i]
            features = self.out_features(kv)
            self.resources_feature[projectid] = features

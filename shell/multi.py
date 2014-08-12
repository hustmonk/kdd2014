#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import csv
import sys
from common import *
from singlefeature import *

__revision__ = '0.1'

def readLabel(filename, dict):
    data_dir = '../data/'
    reader = csv.reader(file(data_dir + filename, 'rb'))
    header = reader.next()
    project_idx = 0
    for i in range(len(header)):
        if header[i] == 'projectid':
            project_idx = i
            break
    for line in reader:
        if header[-1] == 'date_posted' and before(line[-1]):
            continue
        projectid = line[project_idx]
        dict[projectid] = labelToY(line[1:])
feature_space = ""
outcome_dict = {}
test_dict = {}
readLabel("outcomes.csv", outcome_dict)
readLabel("sampleSubmission.csv", test_dict)

resource = SingleFeature("resource")
user = SingleFeature("user")
essay = SingleFeature("essay")
given = SingleFeature("given")
project = SingleFeature("project")

def out_data(filename, dict):
    data_dir = "../result_data/"
    fout = open(data_dir + filename, "w")
    for (pid,v) in dict.items():
        label = v
        if pid not in project.resources_feature:
            continue
        fout.write("%d %s|a %s |b %s |c %s |d %s| e %s\n" % (label, pid, 
            project.resources_feature[pid], resource.resources_feature[pid],
            user.resources_feature[pid], essay.resources_feature[pid],
            given.resources_feature[pid]))

out_data("train.txt", outcome_dict)
out_data("test.txt", test_dict)

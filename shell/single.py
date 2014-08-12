#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import csv
import sys
from essay import *
from common import *
from given import *
from project import *
from resource import *
from usermanage import *

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
single = sys.argv[1]
if single == "essay":
    resource = Essay()
    feature_space = "a"
elif single == "given":
    resource = Given(1)
    feature_space = "b"
elif single == "resource":
    resource = Resource()
    feature_space = "c"
elif single == "user":
    resource = UserManage()
    feature_space = "d"
elif single == "project":
    resource = Project()
    feature_space = "e"
outcome_dict = {}
test_dict = {}
readLabel("outcomes.csv", outcome_dict)
readLabel("sampleSubmission.csv", test_dict)

def out_data(filename, dict):
    data_dir = "../" + single + "/"
    fout = open(data_dir + filename, "w")
    for (pid,v) in dict.items():
        label = v
        if pid not in resource.resources_feature:
            continue
        fout.write("%d %s|%s %s\n" % (label, pid, feature_space, resource.resources_feature[pid].encode("utf-8")))

out_data("train.txt", outcome_dict)
out_data("test.txt", test_dict)

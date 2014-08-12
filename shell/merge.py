#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import csv
from wresource import *
from user import *
#from essay import *
from mm_vectorizer import *
from given import *

__revision__ = '0.1'
type_dict = {}
def before(dat):
    year,month,day = dat.split("-")
    if int(year) < 2010:
        return True
    if int(year) == 2010 and int(month) < 4:
        return True
    return False

for line in open("../data/xp2"):
    if line[0] == '#':
        continue
    arr = line.strip().split("\t")
    type_dict[arr[1]] = arr[2]

def out_features(kv):
    features = ["f"]
    for (k, v) in kv.items():
        if k not in type_dict:
            continue
        if k == "date_posted":
            v = v[5:7]
        if type_dict[k] == 'idf':
            features.append("%s:%.2f" % (k, float(v)/1000))
        elif type_dict[k] == 'id':
            features.append(k+"_"+v.replace(" ", ""))
        elif type_dict[k] == 'english':
            features.append(v)
    #return (" ".join(features)).replace(":", "")
    return (" ".join(features))

def get_total(arr):
    total = 0
    if arr[0] == 't':
        total = 100
    for k in arr[1:]:
        if k == 't':
            total += 1
    return total

def read_file(filename, dict, only_id = False):
    data_dir = '../data/'
    reader = csv.reader(file(data_dir + filename, 'rb'))
    header = reader.next()
    project_idx = 0
    for i in range(len(header)):
        if header[i] == 'projectid':
            project_idx = i
            break

    for line in reader:
        projectid = line[project_idx]
        if only_id:
            #dict[projectid] = line[1]
            dict[projectid] = get_total(line[1:])
            continue
        if header[-1] == 'date_posted' and before(line[-1]):
            continue
        kv = {}
        for i in range(len(header)):
            kv[header[i]] = line[i]
        features = out_features(kv)
        dict[projectid] = features
        #dict[projectid] = line[-1]
        #print "%s | %s" % (projectid, features)

project_dict = {}
outcome_dict = {}
test_dict = {}
essay_dict = {}
resource = Resource()
user = Vectorizer("bak_user")
essay = Vectorizer("bak")
given = Given(1)
read_file("projects.csv", project_dict, only_id = False)
read_file("outcomes.csv", outcome_dict, only_id = True)
read_file("sampleSubmission.csv", test_dict, only_id = True)


def out_data(filename, dict):
    data_dir = "../result_data/"
    fout = open(data_dir + filename, "w")
    for (pid,v) in dict.items():
        label = v
        if pid not in project_dict:
            continue
        fout.write("%d %s|a %s |b %s |c %s |d %s| e %s\n" % (label, pid, 
            project_dict[pid], resource.resources_feature[pid],
            user.resources_feature[pid], essay.resources_feature[pid],
            given.resources_feature[pid]))

out_data("train.txt", outcome_dict)
out_data("test.txt", test_dict)

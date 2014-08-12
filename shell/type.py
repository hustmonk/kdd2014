#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import csv
def is_english(str):
    for ch in str:
        if ch >= 'a' and ch <= 'z':
            return True
        if ch >= 'A' and ch <= 'Z':
            return True
    return False
def read_file(filename):
    data_dir = '../data/'
    reader = csv.reader(file(data_dir + filename, 'rb'))
    header = reader.next()
    project_idx = 0
    for i in range(len(header)):
        if header[i] == 'projectid':
            project_idx = i
            break

    arr = []
    for line in reader:
        arr.append(line)
    lost = ["date_posted","donation_timestamp"]
    for i in range(len(header)):
        type = ""
        if header[i] in lost:
            continue
        s = set()
        for line in arr:
            s.add(line[i])
            if is_english(line[i]):
                type = "english"
        if len(s) < 10:
            type = "id"
        if type == "":
            for line in arr:
                if len(line[i]) == 0:
                    continue
                if float(line[i]) > 10000:
                    type = "id"

        if len(type) > 0:
            print "%d\t%s\t%s\t%s\t%d" % (i, filename, header[i], type, len(s))

files = ["essays.csv", "resources.csv", "projects.csv"]
for filename in files:
    read_file(filename)

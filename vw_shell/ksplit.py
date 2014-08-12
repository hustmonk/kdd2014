#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import random
import csv

__revision__ = '0.1'
fout1 = open("train.txt1", "w")
fout2 = open("train.txt2", "w")
random_select = False
if random_select == False:
    data_dir = '../data/'
    reader = csv.reader(file(data_dir + "projects.csv", 'rb'))
    header = reader.next()
    years = {}
    for line in reader:
        years[line[0]] = int(line[-1].split("-")[0])
    for line in open("train.txt"):
        pid = line.split("|")[0].split(" ")[-1]
        if years[pid] == 2013:
            fout2.write(line)
        else:
            fout1.write(line)
if random_select == True:
    for line in open("train.txt"):
        ran = random.random()
        if ran > 0.1:
            fout1.write(line)
        else:
            fout2.write(line)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Last modified: 
#申请论文信息
#essay info

"""docstring
"""
import csv

__revision__ = '0.1'
class Essay:
    def _normal(self, list):
        new_list = []
        for x in list:
            x = x.lower()
            newx = []
            for ch in x:
                if ('a' <= ch and ch <= 'z') or ('0' <= ch and ch <= '9') or ch == ' ':
                    newx.append(ch)
                else:
                    newx.append(" ")
            new_list.append("".join(newx))
        return new_list

    def __init__(self, debug = False):
        data_dir = '../data/'
        filename = "essays.csv"
        reader = csv.reader(file(data_dir + filename, 'rb'))
        reader.next()
        self.resources_feature = {}
        idx = 0
        for line in reader:
            pid = line[0]
            self.resources_feature[pid] = " ".join(self._normal(line[2:])).decode("utf-8")
            if debug:
                if idx > 1000:
                    break
                idx = idx + 1

if __name__ == '__main__':
    essay = Essay()

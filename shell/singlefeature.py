#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

class SingleFeature:
    def __init__(self, single):
        self.resources_feature = {}
        self.read_file("../" + single + "/train.txt")
        self.read_file("../" + single + "/test.txt")

    def read_file(self,fin):
        for line in open(fin):
            pos = line.strip().find('|')
            pid = line[:pos].split(" ")[-1]
            f = line[pos+2:].strip()
            self.resources_feature[pid] = f

if __name__ == '__main__':
    Vectorizer("essay")

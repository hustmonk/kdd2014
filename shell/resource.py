#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
from common import *
import csv

__revision__ = '0.1'

class Resource:
    def __init__(self):
        data_dir = "../data/"
        filename = 'resources.csv'
        reader = csv.reader(file(data_dir + filename, 'rb'))
        header = reader.next()
        header.append("sum")
        project_idx = 0

        self.resources_feature = {}
        self.resources_infos = {}
        project_resource_type = {}
        for arr in reader:
            pid = arr[1]
            project_resource_type[pid] = arr[4]
            if pid not in self.resources_infos:
                self.resources_infos[pid] = [arr[2:]]
            else:
                self.resources_infos[pid].append(arr[2:])
        pids = []
        feature_info = []
        resources_feature = []
        for (pid, infos) in self.resources_infos.items():
            pids.append(pid)
            features = []
            features.append(len(infos))
            features.append(sum([ float(info[-1]) for info in infos if len(info[-1]) > 0]))
            features.append(max([ float(info[-2]) for info in infos if len(info[-2]) > 0]+[0]))
            sum_total = [ float(info[-2]) * float(info[-1]) for info in infos if len(info[-2]) > 0 and len(info[-1]) > 0]
            features.append(len(sum_total))
            for thre in [10, 20, 30, 40, 50, 60, 70, 80, 100,200,300,400,500,1000,2000,5000,10000]:
                p = sum([1 for k in sum_total if k > thre])
                features.append(features[-1] - p)
                features.append(p)
            features.append(len(sum_total))
            for thre in [10, 20, 30, 40, 50, 60, 70, 80, 100,200,300,400,500,1000,2000,5000,10000]:
                p = sum([1 for info in infos if len(info[-2]) > 0 and float(info[-2]) > thre])
                features.append(features[-1] - p)
                features.append(p)
            features.append(sum(sum_total))
            feature_info.append(features)
            resources_feature.append([])

        for i in range(len(feature_info[1])):
            news = []
            for k in feature_info:
                news.append(k[i])
            old_feature,kids = idf(news)
            for j in range(len(feature_info)):
                pid = pids[j]
                rtype = project_resource_type[pid]
                #resources_feature[j].append("%d:%.2f" % (i,old_feature[j]))
                resources_feature[j].append(str(i)+"_"+kids[j])
                #resources_feature[j].append("R%s%d:%.2f" % (rtype,i,old_feature[j]))
                if kids[j] != '0':
                    resources_feature[j].append("R"+rtype + str(i)+"_"+kids[j])

        #expand(resources_feature)
        for j in range(len(feature_info)):
            pid = pids[j]
            f1 = resources_feature[j]
            #f2 = [ str(i) + infos[0][2]+":"+str(features[i]) for i in range(len(features))]
            #self.resources_feature[pid] = " ".join([ str(i) +":"+str(features[i]) for i in range(len(features))])
            self.resources_feature[pid] = " ".join(f1)

if __name__ == '__main__':
    resource = Resource()





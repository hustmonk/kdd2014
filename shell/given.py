#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import csv
from common import *
__revision__ = '0.1'

class Given:
    def get_key(self, kidxs, line):
        if type(kidxs) == type(1):
            return line[kidxs]
        else:
            return "_".join([line[kidx] for kidx in kidxs])

    def __init__(self, label_idx):
        data_dir = "../data/"
        reader = csv.reader(file(data_dir + "outcomes.csv", 'rb'))
        excitings = {}
        for line in reader:
            if line[label_idx] == 't':
                excitings[line[0]] = 1
            else:
                excitings[line[0]] = 0
        filename = 'projects.csv'
        reader = csv.reader(file(data_dir + filename, 'rb'))
        header = reader.next()
        #project_areas = [1, 2, 6]
        #project_areas = [1]
        project_areas = [1, 2, 6, 7, [32,33,28,27],[28,27,26,25],[25,24,23],[25,22,21],[20,19,18,17],[18,17,16,15,14],[9,12,13,14]]
        pids = {}
        teatcher_info = {}
        project_info = []
        for line in reader:
            if before(line[-1]):
                continue
            pid = line[0]
            pids[pid] = line[1]
            keys = []
            for i in range(len(project_areas)):
                k = self.get_key(project_areas[i], line)
                keys.append(k)
            teatcher_info[line[1]] = keys
            project_info.append(line)

        g_project_num_in_area = [{} for i in range(len(project_areas))]
        g_excitings_project_num_in_area = [{} for i in range(len(project_areas))]
        pid_acctid = {}
        for line in csv.reader(file(data_dir + "donations.csv", 'rb')):
            pid,acctid = line[1:3]
            if pid not in pids or acctid not in teatcher_info:
                continue
            info = teatcher_info[acctid]
            if pid not in pid_acctid:
                pid_acctid[pid] = set()
            pid_acctid[pid].add(acctid)
            #if acctid == "d9bd5804bf8e0ea3a388888cd15ab7d7":
            #    print excitings.get(pid, 0)
            if excitings.get(pid, 0) == 1:
                for i in range(len(project_areas)):
                    g_excitings_project_num_in_area[i][info[i]] = g_excitings_project_num_in_area[i].get(info[i], 0) + 1
            for i in range(len(project_areas)):
                g_project_num_in_area[i][info[i]] = g_project_num_in_area[i].get(info[i], 0) + 1
        filename = 'projects.csv'
        reader = csv.reader(file(data_dir + filename, 'rb'))
        header = reader.next()
        feature_info = []
        resources_feature = []
        pids = []
        """
        for (k, v) in g_project_num_in_area[0].items():
            print k,v,g_excitings_project_num_in_area[0].get(k, 0)
        exit()
        """
        local_project_num_in_area = [{} for i in range(len(project_areas))]
        local_excitings_project_num_in_area = [{} for i in range(len(project_areas))]
        for i in range(len(project_info)):
            line = project_info[-(i+1)]
            if before(line[-1]):
                continue
            pid = line[0]
            pids.append(pid)
            features = []
            for i in range(len(project_areas)):
                k = self.get_key(project_areas[i], line)
                num = g_project_num_in_area[i].get(k, 0)
                ex_num = g_excitings_project_num_in_area[i].get(k, 0)
                """
                features.append(num)
                features.append(ex_num)
                features.append((ex_num+0.05)/(num+1))
                """
                num = local_project_num_in_area[i].get(k, 0)
                ex_num = local_excitings_project_num_in_area[i].get(k, 0)
                features.append(num)
                features.append(ex_num)
                features.append((ex_num+0.05)/(num+1))
            
            for acctid in pid_acctid.get(pid, []):
                info = teatcher_info[acctid]
                if excitings.get(pid, 0) == 1:
                    for i in range(len(project_areas)):
                        local_excitings_project_num_in_area[i][info[i]] = local_excitings_project_num_in_area[i].get(info[i], 0) + 1
                for i in range(len(project_areas)):
                    local_project_num_in_area[i][info[i]] = local_project_num_in_area[i].get(info[i], 0) + 1
            feature_info.append(features)
            resources_feature.append([])

        """
        for k in local_excitings_project_num_in_area:
            print k
        exit()
        """
        #invert features
        for i in range(len(feature_info[0])):
            news = []
            print i, "XXXXXXXXX"
            for k in feature_info:
                news.append(k[i])
            old_feature,kids = idf(news)
            if len(old_feature) == 0:
                continue
            for j in range(len(feature_info)):
                pid = pids[j]
                if len(old_feature) > 0:
                    resources_feature[j].append("%d:%.2f" % (i,old_feature[j]))
                resources_feature[j].append(str(i)+"_"+kids[j])
                #resources_feature[j].append("%s_%d:%.2f" % (first,i,old_feature[j]))
                #resources_feature[j].append(str(first)+"_"+str(i)+"_"+kids[j])

        self.resources_feature = {}
        #expand(resources_feature)
        for j in range(len(feature_info)):
            pid = pids[j]
            f1 = resources_feature[j]
            self.resources_feature[pid] = " ".join(f1)

if __name__ == '__main__':
    user = Given(1)

#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import csv
from common import *
__revision__ = '0.1'

class User:
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
        #print header[1], header[2], header[6]
        infos = []
        #project_areas = [1, 2, 6, 7, [32,33,28,27],[28,27,26,25],[25,24,23],[25,22,21],[20,19,18,17],[18,17,16,15,14],[9,12,13,14]]
        project_areas = [2, 6, 7, [32,33,28,27],[28,27,26,25],[25,24,23],[25,22,21],[20,19,18,17],[18,17,16,15,14],[9,12,13,14]]
        #project_areas = [1, 2, 6]
        #teacher_areas = project_areas[1:]
        teacher_areas = project_areas
        g_project_num_in_area = [{} for i in range(len(project_areas))]
        g_only_project_num_in_area = [{} for i in range(len(project_areas))]
        g_excitings_project_num_in_area = [{} for i in range(len(project_areas))]
        g_teacher_num_in_area = [{} for i in range(len(teacher_areas))]
        for line in reader:
            if before(line[-1]):
                continue
            pid = line[0]
            for i in range(len(project_areas)):
                k = self.get_key(project_areas[i], line)
                g_project_num_in_area[i][k] = g_project_num_in_area[i].get(k, 0) + 1
                if excitings.get(pid, 0) == 1:
                    g_excitings_project_num_in_area[i][k] = g_excitings_project_num_in_area[i].get(k, 0) + 1
            teacher = line[1]
            for i in range(len(teacher_areas)):
                k = self.get_key(teacher_areas[i], line)
                if k not in g_teacher_num_in_area[i]:
                    g_teacher_num_in_area[i][k] = {}
                g_teacher_num_in_area[i][k][teacher] = 1
            infos.append(line)

        local_project_num_in_area = [{} for i in range(len(project_areas))]
        local_excitings_project_num_in_area = [{} for i in range(len(project_areas))]
        local_teacher_num_in_area = [{} for i in range(len(teacher_areas))]

        feature_info = []
        pids = []
        resources_feature = []
        first_pids = {}
        for i in range(len(infos)):
            line = infos[len(infos) - 1 - i]
            pid = line[0]
            pids.append(pid)
            features = []
            for i in range(len(project_areas)):
                k = self.get_key(project_areas[i], line)
                features.append(g_project_num_in_area[i][k])
                #features.append((g_excitings_project_num_in_area[i].get(k, 0) + 0.1)/(1+g_project_num_in_area[i].get(k, 0)))
            for i in range(len(teacher_areas)):
                k = self.get_key(teacher_areas[i], line)
                features.append(len(g_teacher_num_in_area[i][k]))

            #print teacher, global_excitings_teacher, school,global_excitings_school, city,global_excitings_city
            #if local_project_num_in_area[0].get(line[1], 0) == 0:
            #    print line[-1]

            if label_idx == 1:
                for i in range(len(project_areas)):
                    k = self.get_key(project_areas[i], line)
                    features.append(local_project_num_in_area[i].get(k, 0))
                    features.append((local_excitings_project_num_in_area[i].get(k, 0) + 0.1)/(1+local_project_num_in_area[i].get(k, 0)))
                    if pid not in excitings:
                        continue
                    local_project_num_in_area[i][k] = local_project_num_in_area[i].get(k, 0) + 1
                    if excitings.get(pid, 0) == 1:
                        local_excitings_project_num_in_area[i][k] = local_excitings_project_num_in_area[i].get(k, 0) + 1
                for i in range(len(teacher_areas)):
                    k = self.get_key(teacher_areas[i], line)
                    teacher = line[1]
                    if k not in local_teacher_num_in_area[i]:
                        local_teacher_num_in_area[i][k] = {}
                    local_teacher_num_in_area[i][k][teacher] = 1
                    features.append(len(local_teacher_num_in_area[i][k]))

            if line[1] not in local_project_num_in_area[0] or local_project_num_in_area[0][line[1]] == 1:
                first_pids[pid] = 1

            feature_info.append(features)
            #resources_feature.append([line[i].replace(" ","") for i in project_areas])
            resources_feature.append([])

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
                first = False
                if pid in first_pids:
                    first = True
                #resources_feature[j].append("%s_%d:%.2f" % (first,i,old_feature[j]))
                #resources_feature[j].append(str(first)+"_"+str(i)+"_"+kids[j])

        self.resources_feature = {}
        #expand(resources_feature)
        for j in range(len(feature_info)):
            pid = pids[j]
            f1 = resources_feature[j]
            self.resources_feature[pid] = " ".join(f1)

if __name__ == '__main__':
    user = User()

import math
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.stats import fisher_exact
from common import *
from essay import *
import nltk
import re

class Vectorizer(object):
    max_features = 5000

    def __init__(self):
        self.fit_done = False
        self.essay = Essay()
        self.vocab_dict_file = "../data/vocab.dict"
        cache = 1
        if  cache == 0:
            texts,scores = self.read_train_data()
            self.build_vocab(texts, scores)
        else:
            self.read_vocab_dict()
        self.fit()
        self.get_features()

    def read_train_data(self):
        data_dir = '../data/'
        reader = csv.reader(file(data_dir + "outcomes.csv", 'rb'))
        kv = {}
        print "kv"
        for line in reader:
            kv[line[0]] = line[1]
        print "essay"

        print "train data"
        train_data = []
        for line in csv.reader(file(data_dir + "projects.csv", 'rb')):
            if line[-1] == 'date_posted' and before(line[-1]):
                continue
            if line[0] not in kv:
                continue
            label = 0
            if kv[line[0]] == 't':
                label = 1
            train_data.append([self.essay.resources_feature[line[0]], label])
        texts = [x[0] for x in train_data]
        scores = [x[1] for x in train_data]
        return texts,scores

    def build_vocab(self, input_text, input_scores):
        df = {}
        good_scores = {}
        reg = re.compile("[A-Za-z]+")
        for i in range(len(input_text)):
            if i %1000 == 0:
                print i
                print input_text[i]
            words = reg.findall(input_text[i].lower())
            for word in set(words):
                df[word] = df.get(word, 0) + 1
                if input_scores[i]:
                    good_scores[word] = good_scores.get(word, 0) + 1
        good_num = sum(input_scores)
        bad_num = len(input_scores) - good_num

        pvalues = []
        for word in df:
            present = df[word]
            if present < 10:
                pvalues.append(1000000)
                continue
            missing = len(input_scores) - present
            good_lcol_present = good_scores.get(word, 0)
            good_lcol_missing = good_num - good_lcol_present
            bad_lcol_present = present - good_lcol_present
            bad_lcol_missing = bad_num - bad_lcol_present

            ent = self._entropy(good_lcol_present, good_lcol_present + bad_lcol_present) \
                    + self._entropy(bad_lcol_present, good_lcol_present + bad_lcol_present) \
                    + self._entropy(good_lcol_missing, good_lcol_missing + bad_lcol_missing) \
                    + self._entropy(bad_lcol_missing, good_lcol_missing + bad_lcol_missing)
            pvalues.append(-1 * ent)
            print word,good_lcol_present,good_lcol_missing,bad_lcol_present,bad_lcol_missing,ent

        col_inds = range(0, len(pvalues))
        p_frame = np.array([col_inds, pvalues]).transpose()
        p_frame = p_frame[p_frame[:, 1].argsort()]

        rows = p_frame.shape[0]
        selection = self.max_features
        if rows < selection:
            selection = rows

        getVar = lambda searchList, ind: [searchList[int(i)] for i in ind]
        self.vocab = getVar(df.keys(), p_frame[:, 0][:selection])

        fout = open(self.vocab_dict_file, "w")
        print "XXX"
        for k in p_frame:
            print k
        for k in self.vocab:
            fout.write("%s\n" % k)
            print k

    def read_vocab_dict(self):
        self.vocab = []
        for line in open(self.vocab_dict_file):
            self.vocab.append(line.strip())

    def fit(self):
        self.vectorizer = {}
        for k in self.vocab:
            self.vectorizer[k] = len(self.vectorizer)
        self.fit_done = True

    def _entropy(self, a, b):
        if a == 0:
            return 0
        return a * math.log(a/float(b))

    def get_features(self):
        self.resources_feature = {}
        if not self.fit_done:
            raise Exception("Vectorizer has not been created.")
        reg = re.compile("[A-Za-z]+")
        for (pid, essay) in self.essay.resources_feature.items():
            words = reg.findall(essay.lower())
            v = {}
            for word in words:
                if word in self.vectorizer:
                    idx = self.vectorizer[word]
                    v[idx] = 1
            v1 = []
            for i in v:
                v1.append("%d" % i)
            v1.append("wordC:%.3f" % (len(words)/100.0))
            v1.append("essaL:%.3f" % (len(essay)/500.))
            self.resources_feature[pid] = " ".join(v1)
        del self.essay

if __name__ == '__main__':
    essay = Vectorizer()


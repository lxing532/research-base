from gensim.models import doc2vec
from collections import namedtuple
import csv
import re
import string
import random
import numpy as np
from numpy import linalg as la

#implement para2vec with gensim

#euclid similarity
def euclidSimilar(inA,inB):
    return 1.0/(1.0+la.norm(inA-inB))

#cosin similarity
def cosSimilar(inA,inB):
    inA=np.mat(inA)
    inB=np.mat(inB)
    num=float(inA*inB.T)
    denom=la.norm(inA)*la.norm(inB)
    return 0.5+0.5*(num/denom)

#reader = csv.reader(open('/users/xinglinzi/desktop/test.txt'))
'''
count = 0
data = ''
for row in reader:
    count += 1
    if count>301:
        break
    else:
        data += row[1]

'''
data_list = []
for line in open('/users/xinglinzi/desktop/test.txt'):
    data_list.append(line.strip())

# separate long string into sentences based on '.?!'
#sentenceEnders = re.compile('[.?!]')
#data_list = sentenceEnders.split(data)
#print(data_list)
# eliminate sentence less than 3 words and all the punctuation
LabelDoc = namedtuple('LabelDoc','words tags')
exclude = set(string.punctuation)
all_docs = []
count = 0
for sen in data_list:
    word_list = sen.split()
    if len(word_list) < 3:
        continue
    tag = ['SEN_'+str(count)]
    count += 1
    sen = ''.join(ch for ch in sen if ch not in exclude)
    all_docs.append(LabelDoc(sen.split(),tag))
#print(all_docs)
model = doc2vec.Doc2Vec(size=200, alpha=0.025,min_alpha=0.025)
model.build_vocab(all_docs)
for epoch in range(10):
    model.train(all_docs)
    model.alpha -= 0.002
    model.min_alpha = model.alpha

model.save('model.doc2vec')
doc_id = np.random.randint(model.docvecs.count)
print doc_id
sims = model.docvecs.most_similar(doc_id, topn=model.docvecs.count)
print('TARGET' , all_docs[doc_id].words)
count = 0
for i in sims:
    if count > 8:
        break
    pid = int(string.replace(i[0], "SEN_", ""))
    print(i[0],": ", all_docs[pid].words)
    count += 1
vec1_list = [];vec2_list = [];vec3_list = [];vec4_list = []
for i in range(10):
    vec1_list.append(model.docvecs[i])
for i in range(10,20):
    vec2_list.append(model.docvecs[i])
for i in range(20,30):
    vec3_list.append(model.docvecs[i])
for i in range(30,40):
    vec4_list.append(model.docvecs[i])
count = 0
v1 = 0;v2 = 0;v3 = 0;v4 = 0

for j in range(10):
    v1 += vec1_list[j]
for j in range(10):
    v2 += vec2_list[j]
for j in range(10):
    v3 += vec3_list[j]
for j in range(10):
    v4 += vec4_list[j]

print(cosSimilar(v1,v2))
print(cosSimilar(v1,v3))
print(cosSimilar(v1,v4))
print(cosSimilar(v2,v3))
print(cosSimilar(v2,v4))
print(cosSimilar(v3,v4))




from gensim.models import doc2vec
from collections import namedtuple
import csv
import re
import string

# choose first 300 lines in file and concatenate together
reader = csv.reader(open('../data/testdata.csv'))
count = 0
data = ''
for row in reader:
    count += 1
    if count>301:
        break
    else:
        data += row[1]

# separate long string into sentences based on '.?!'
sentenceEnders = re.compile('[.?!]')
data_list = sentenceEnders.split(data)
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

model = doc2vec.Doc2Vec(alpha=0.025,min_alpha=0.025)
model.build_vocab(all_docs)
for epoch in range(10):
    model.train(all_docs)
    model.alpha -= 0.002
    model.min_alpha = model.alpha

model.save('model.doc2vec')

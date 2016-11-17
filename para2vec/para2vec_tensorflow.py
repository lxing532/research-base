from gensim.models import doc2vec
from collections import namedtuple
import csv
import re
import string
import collections
import numpy as np
import random

def build_dataset(inputs, min_freq):
    words = []
    for i in inputs:
        for j in i.words:
            words.append(j)
    count_org = [['UNK',-1]]
    count_org.extend(collections.Counter(words).most_common())
    count = [['UNK',-1]]
    for word,c in count_org:
        word_tuple = [word,c]
        if word == "UNK":
            count[0][1] = c
            continue

        if c>min_freq:
            count.append(word_tuple)
    dictionary = dict()
    for word,_ in count:
        dictionary[word] = len(dictionary)
    data = []
    unk_count = 0
    for tup in inputs:
        word_data = []
        for word in tup.words:
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0
                unk_count += 1
            word_data.append(index)
        data.append(LabelDoc(word_data,tup.tags))
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(),dictionary.keys()))
    return data,count,dictionary,reverse_dictionary

def batch(size,skip,skip_window):

    global word_index
    global sentence_index
    assert size%skip == 0
    assert skip<=2*skip_window

    batch = np.ndarray(shape=(size,skip),dtype=np.int32)
    labels = np.ndarray(shape=(size,1),dtype=np.int32)
    para_labels = np.ndarray(shape=(size,1),dtype=np.int32)
    span = 2*skip_window+1
    buffer = collections.deque(maxlen=span)

    for i in range(span):
        buffer.append(data[sentence_index].words[word_index])
        sen_len = len(data[sentence_index].words)
        if sen_len-1 == word_index:
            word_index = 0
            sentence_index = (sentence_index+1)%len(data)
        else:
            word_index += 1
    for i in range(batch):
        target = skip_window
        targettoavoid = [skip_window]
        batch_temp = np.ndarray(shape=(skip),dtype=np.int32)
        for j in range(skip):
            while target in targettoavoid:
                target = random.randint(0,span-1)
            targettoavoid.append(target)
            batch_temp[j] = buffer[target]
        batch[i] = batch_temp
        labels[i,0] = buffer[skip_window]
        para_labels[i,0] = sentence_index
        buffer.append(data[sentence_index].words[word_index])
        sen_len = len(data[sentence_index].words)
        if sen_len-1 == word_index:
            word_index = 0
            sentence_index = (sentence_index+1)%len(data)
        else:
            word_index += 1
    return batch,labels,para_labels

if __name__ == '__main__':

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

    data,count,dictionary,reverse_dictionary = build_dataset(all_docs,0)
    print(data)
    print(count)
    print(dictionary)

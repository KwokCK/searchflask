#!/usr/bin/env python
# -*- coding: utf-8 -*
import gensim
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

model = gensim.models.KeyedVectors.load_word2vec_format("wiki.en.text.vector", binary=False)
#model = gensim.models.KeyedVectors.load_word2vec_format("wiki.en.text.vector", binary=False)
#models = gensim.models.Word2Vec.load("wiki.en.text.vector", binary=False)

## Test printing similar
#print(model.wv.most_similar(positive='hamlet'))

## Test printing man and woman
#print('King - man + woman:')

#print('')
#for word, sim in model.most_similar(positive=['woman', 'king'], negative=['man']):
#for word, sim in model.most_similar(positive=['japan', 'paris'], negative=['france']):
#    print('\"%s\"\t- similarity: %g' % (word, sim))
#print('')

#print('Similarity between a and b:')
#print(model.similarity('china', 'japan'))

while True:
    try:
        query = input("Entry word with ' ' \n")
        query_list = query.split(",")
        print len(query_list)

        if len(query_list) == 1:
            print("The top 10 similiar word is...:")
            res = model.most_similar(query_list[0], topn=10)
            for item in res:
                print(item[0] + "," + str(item[1]))
        elif len(query_list) == 2:
            print("The similiarity of these two words are...:")
            res = model.similarity(query_list[0], query_list[1])
            print(res)
        else:
            print("%s = %s，%s = ..." % (query_list[0], query_list[1], query_list[2]))
            res = model.most_similar(positive=[query_list[2], query_list[1]], negative=[query_list[0]], topn=5)
            for item in res:
                print(item[0] + "," + str(item[1]))
    except Exception as e:
        print("Error:" + repr(e))

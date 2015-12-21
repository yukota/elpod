# -*- coding: utf-8 -*-

from natto import MeCab
from nltk.tokenize.regexp import WhitespaceTokenizer, RegexpTokenizer
from nltk.corpus.reader import PlaintextCorpusReader

import codecs
import os

from gensim.models import word2vec


class Semantics:
    def __init__(self):
        # mecab setup
        os.environ['MECAB_PATH'] = '/usr/local/lib/libmecab.dylib'
        os.environ['MECAB_CHARSET'] = 'utf-8'
        pass

    def get_similar_words(self, src_message):
        noums = self.__parse_to_norms(src_message)
        for noum in noums:
            print(noum)
        # self.create_and_save_word2vec_model()
        sim_words = self.__search_similar_words(noums)
        print(sim_words)
        return sim_words


    def __parse_to_norms(self, message):
        option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
        with MeCab(options=option) as me_cab:
            print(me_cab)
            words = me_cab.parse(message, as_nodes=True)
            return [word.surface for word in words if 36 <= word.posid <= 67]

    def create_and_save_word2vec_model(self):
        corpus = word2vec.Text8Corpus('./corpus/corpus.txt')
        model = word2vec.Word2Vec(corpus, min_count=5)
        model.save('./model/word2vec2.model2')


    def __search_similar_words(self, words):
        model = word2vec.Word2Vec.load('./model/word2vec.model')
        try:
            words = [word[0] for word in model.most_similar(positive=words, topn=4)]
        except KeyError:
            return None
        return words

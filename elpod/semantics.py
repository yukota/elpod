# -*- coding: utf-8 -*-

from natto import MeCab
import logging
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
        # self.create_and_save_word2vec_model()
        similar_words = self.__search_similar_words(noums)
        return similar_words


    def __parse_to_norms(self, message):
        option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
        with MeCab(options=option) as me_cab:
            words = me_cab.parse(message, as_nodes=True)
            return [word.surface for word in words if 36 <= word.posid <= 67]

    def create_and_save_word2vec_model(self):
        corpus = word2vec.Text8Corpus('./corpus/corpus.txt')
        model = word2vec.Word2Vec(corpus, min_count=5)
        model.save('./model/word2vec2.model2')


    def __search_similar_words(self, words):
        model = word2vec.Word2Vec.load('./model/word2vec.model')
        logging.debug("search similar words of {0}".format(words))
        try:
            similar_words = [word[0] for word in model.most_similar(positive=words, topn=4)]
        except KeyError:
            return None
        logging.debug("result of search similar words:{0}".format(similar_words))
        return similar_words

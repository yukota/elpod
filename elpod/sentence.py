# -*- coding: utf-8 -*-

from cytoolz import sliding_window
from itertools import chain, permutations
from collections import namedtuple
import logging
import os

from natto import MeCab
import networkx
import matplotlib.pyplot as plt


class Sentence:
    def __init__(self):
        # mecab setup
        os.environ['MECAB_PATH'] = '/usr/local/lib/libmecab.dylib'
        os.environ['MECAB_CHARSET'] = 'utf-8'

        self.Node = namedtuple('Node', ('posid', 'surface'))
        self.START_NODE = self.Node(posid=-1, surface='')
        self.END_NODE = self.Node(posid=-2, surface='')


    def learn(self, sentences):
        logging.debug("learn")
        posid_list = self._get_posid_seq(sentences)

        # create grammer network.
        self._grammer_graph = self._create_grammer_network(posid_list)
        # self._draw()


    def generate(self, similar_words):
        logging.debug("generate{0}".format(similar_words))
        posids = self._get_posid(similar_words)
        construnts = []
        for posid in posids:
            if posid in self._grammer_graph:
                construnts.append(posid)

        # posid!,0で文字列を生成、最短文字列を採用する。
        pos_via_points = permutations(construnts)
        sentences = []
        for pos_via_point in pos_via_points:
            # costが低い方が発生率が高い
            cost, path = self._search_grammer_path(pos_via_point)
            sentence = ''
            for node in path:
                sentence += node.surface
            logging.debug("---------found paths---------")
            logging.debug("path:{0}".format(path))
            logging.debug("cost:{0}".format(cost))
            logging.debug("sentence:{0}".format(sentence))
            logging.debug("---------found paths---------")
            sentences.append((cost, sentence))

        # コスト最小のものを選択
        generated = min(sentences, key=(lambda x: x[0]))
        return generated[1]

    def _search_grammer_path(self, pos_via_point):
        pos_via_and_end = (self.START_NODE,) + pos_via_point + (self.END_NODE,)
        paths = []
        cost = 0
        for network_start_end in sliding_window(2, pos_via_and_end):
            path = networkx.bidirectional_dijkstra(self._grammer_graph, network_start_end[0], network_start_end[1])
            cost += path[0]
            node_path = path[1][1:]
            paths += node_path
        paths.pop()
        return cost, paths


    def _create_grammer_network(self, posid_list):
        # cout node and edge
        node = set()
        for posid in chain.from_iterable(posid_list):
            node.add(posid)

        edge_weight_dict = {}
        for sentence in posid_list:
            for one_edge in sliding_window(2, sentence):
                edge_weight_dict[one_edge] = edge_weight_dict.get(one_edge, 1) + 1

        max_weight = max(edge_weight_dict.values())
        # NetworkX上、weightはcost扱いなので、出現頻度が高いものが低コストになるようにする

        # create direct network
        graph = networkx.DiGraph()
        graph.add_nodes_from(node)
        for edge, weight in edge_weight_dict.items():
            # 最低コストを1とする
            cost = max_weight - weight + 1
            graph.add_edge(edge[0], edge[1], weight=cost)
        return graph

    def _get_posid_seq(self, sentences):
        option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
        posid_list = []
        with MeCab(options=option) as me_cab:
            for sentence in sentences:
                words = me_cab.parse(sentence, as_nodes=True)
                # 先頭が-1,終端が-2とする
                one_work_posid = [self.START_NODE]
                for word in words:
                    node = self.Node(posid=word.posid, surface=word.surface)
                    one_work_posid.append(node)

                one_work_posid.append(self.END_NODE)
                posid_list.append(one_work_posid)
        return posid_list

    def _get_posid(self, words):
        node_list = []
        option = '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'
        with MeCab(options=option) as me_cab:
            for word in words:
                sw = me_cab.parse(word, as_nodes=True)
                for w in sw:
                    if w.posid != 0:
                        node = self.Node(posid=w.posid, surface=w.surface)
                        node_list.append(node)

        return node_list

    def _draw(self):
        networkx.draw_spring(self._grammer_graph, iterations=20, with_labels=True)
        plt.show()

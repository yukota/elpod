# -*- coding: utf-8 -*-

from unittest import TestCase
from nose.tools import eq_
from sentence import Sentence


class TestSemantics(TestCase):
    def setUp(self):
        self.sentence = Sentence()

    def test_generate(self):
        #self.sentence.generate(['東京', 'とは'])
        pass

    def test_get_posid(self):
        self.sentence._get_posid(['東京', 'とは'])

# -*- coding: utf-8 -*-

from unittest import TestCase
from nose.tools import eq_
from semantics import Semantics
import config


class TestSemantics(TestCase):
    def setUp(self):
        self.semantics = Semantics()

    def test_generate_sentence_with_keyword(self):
        self.semantics._generate_sentence_with_keyworkd(['東京', 'とは'])

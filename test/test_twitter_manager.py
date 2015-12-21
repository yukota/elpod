# -*- coding: utf-8 -*-

from unittest import TestCase
from nose.tools import eq_
from twitter_manager import Twitter
import config



class TestTwitter(TestCase):
    def setUp(self):
        self.twitter = Twitter(consumer_key=config.CONSUMER_KEY, consumer_secret=config.CONSUMER_SECRET,
                               access_token_key=config.ACCESS_TOKEN, access_token_secret=config.ACCESS_TOKEN_SECRET)

    def test_is_include_symbol(self):
        eq_(self.twitter._is_include_symbol('hogehoge'), False)
        eq_(self.twitter._is_include_symbol('hogehoge #fuga'), True)
        eq_(self.twitter._is_include_symbol('hogehoge http://www.google.com'), True)
        eq_(self.twitter._is_include_symbol('このまま眠りつづけて死ぬ #nemuritsuzuketeshinu'), True)

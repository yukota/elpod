#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from twitter_manager import Twitter
from semantics import Semantics
from sentence import Sentence

import config as config

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    # update mimicry model tweet
    twitter = Twitter(consumer_key=config.CONSUMER_KEY, consumer_secret=config.CONSUMER_SECRET,
                      access_token_key=config.ACCESS_TOKEN, access_token_secret=config.ACCESS_TOKEN_SECRET)
    twitter.update_status(config.MIMICRY_MODEL)

    # setup natural language recognition env.
    message = twitter.get_latest_status_text(config.MIMICRY_MODEL)
    if message is None:
        logging.error("Mimicry target's tweet is None.")
        exit()
    semantics = Semantics()
    similar_words = semantics.get_similar_words(message)
    train_posts = twitter.get_all_status_text()
    sentence = Sentence()
    sentence.learn(train_posts)
    generated_message = sentence.generate(similar_words)
    twitter.post(generated_message)







# -*- coding: utf-8 -*-
import twitter
import re
import glob
import json
import logging
from dateutil import parser
from storage import Storage


class Twitter:
    def __init__(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        self.__storage = Storage()
        if self.__storage.is_initial():
            self._initialize_storage()

        self.__api = twitter.Api(consumer_key=consumer_key,
                                 consumer_secret=consumer_secret,
                                 access_token_key=access_token_key,
                                 access_token_secret=access_token_secret)

    def post(self, message):
        logging.info("post to twitter:%s" % message)
        #self.__api.PostUpdate(message)

    def update_status(self, screen_name):
        """
        Update mimicry target status.
        updated status are stored to storage.
        """
        status_id = self.__storage.get_latest_status_id(screen_name)
        if status_id is None:
            statuses = self.__api.GetUserTimeline(screen_name=screen_name, include_rts=False, exclude_replies=True)
        else:
            statuses = self.__api.GetUserTimeline(screen_name=screen_name, since_id=status_id, include_rts=False,
                                                  exclude_replies=True)
        for status in statuses:
            post_user = status.user.screen_name
            status_id = status.id
            posted_at = parser.parse(status.created_at)
            text = status.text
            if self._is_include_symbol(text):
                continue

            self.__storage.add_status(post_user, status_id, posted_at, text)

    def _is_include_symbol(self, text):
        is_hash_tag = re.search('#', text)
        if is_hash_tag is not None:
            return True
        is_url = re.search('http', text)
        if is_url is not None:
            return True
        is_reply = re.search('@', text)
        if is_reply is not None:
            return True

        return False

    def get_latest_status_text(self, screen_name):
        return self.__storage.get_latest_status_text(screen_name)

    def get_all_status_text(self):
        return self.__storage.get_all_status_text()


    def _initialize_storage(self):
        # read twitter's js archive and register
        file_paths = glob.glob('./corpus/twitter/*.js')
        for file_path in file_paths:
            self._register_archive(file_path)

    def _register_archive(self, file_path):
        with open(file_path, 'r') as json_file:
            json_file.readline()
            tweets = json.load(json_file)
            for status in tweets:
                text = status['text']
                status_id = status['id']
                posted_at = parser.parse(status['created_at'])
                if self._is_include_symbol(text):
                    continue
                self.__storage.add_status(text, status_id, posted_at, text)

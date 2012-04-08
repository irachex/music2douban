#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import codecs
import urllib
import json

from client import DoubanOAuth

ME_URI = "/people/@me"

class DoubanRobot(object):
    user = None
    def __init__(self, key=None, secret=None, api_key=None, api_secret=None):
        if api_key and api_secret:
            self.client = DoubanOAuth(api_key, api_secret)
        else:
            self.client = DoubanOAuth()
        if key and secret:
            self.client.login(key, secret)
    
    def get(self, url, param=None):
        return self.client.request('GET', url, param=param)

    def put(self, url, body=None):
        return self.client.request('PUT', url, body and body.encode('utf-8'))

    def post(self, url, body=None):
        return self.client.request('POST', url, body and body.encode('utf-8'))
    
    def get_auth_url(self):
        return self.client.auth_url()
    
    def get_access_token(self, token_key, token_secret):
        self.client.get_access_token(token_key, token_secret)
        
    def get_current_user(self):
        jsondata = self.get(ME_URI, param={"alt":"json"}).read()
        print jsondata
        data = json.loads(jsondata)
        return data
        
    @property
    def token_key(self):
        return self.client.token_key
    
    @property
    def token_secret(self):
        return self.client.token_secret


def escape(s):
    return urllib.quote(s, safe='~')
        

def test():
    robot = DoubanRobot(api_key=DB_API_KEY, api_secret=DB_API_SECRET)
    douban_url = doubanbot.get_auth_url()
    
    
    #robot.fetch_mails()
        
    
if __name__ == '__main__':
    test()
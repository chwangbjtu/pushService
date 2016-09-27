# -*-coding:utf-8 -*-
from singleton import Singleton
from api import http_client

class TokenMgr(Singleton):
    def init_data(self):
        self._delete_tokens = []
        self._client = http_client.HttpClient()
        
    def add_delete_token(self, token):
        self._delete_tokens.append(token)
        
    def delete_token(self):
        self._client.del_token(self._delete_tokens)
        self._delete_tokens = []
        
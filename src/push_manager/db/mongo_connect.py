# -*-coding:utf-8 -*-
import traceback
from tornado import log
from pymongo import MongoClient
from pymongo.collection import ReturnDocument

import sys
sys.path.append('.')

#refer: http://api.mongodb.org/python/current/api/pymongo/
class MongoConnect(object):
    
    def __init__(self, urls, db, user, passwd):
        self._urls = urls
        self._dbname = db
        self._username = user
        self._passwd = passwd
        self._connected = False
        self.connect()

    def connect(self):
        try:
            urls = []
            if self._urls:
                url_tmp = self._urls.split(';')
                for url in url_tmp:
                    url = url.strip()
                    urls.append(url)
            self._mongo = MongoClient(urls)
            self._db = getattr(self._mongo, self._dbname)
            self._db.authenticate(self._username, self._passwd)
            self._connected = True
        except Exception, err:
            self._connected = False
            log.app_log.error(traceback.format_exc())

    def is_connected(self):
        return self._connected

    '''
        db.test.delete_one({'x': 1})
        [{'x':1,'_id':0},{'x':1,'_id':1}] -> [{'x':1,'_id':1}]
    '''
    def delete_one(self, coll_name, filter):
        try:
            if self._connected:
                return self._db[coll_name].delete_one(filter)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
        db.test.delete_many({'x': 1})
        [{'x':1,'_id':0},{'x':1,'_id':1}] -> []
    '''
    def delete_many(self, coll_name, filter):
        try:
            if self._connected:
                return self._db[coll_name].delete_many(filter)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    Parameters:
        filter: A query that matches the document to update.
        update: The modifications to apply.
        upsert (optional): If True, perform an insert if no documents match the filter.
    Examples:
        db.test.update_one({'x': 1}, {'$inc': {'x': 3}})
        {'x':1, '_id':0} -> {'x':4, '_id':0}
        {'x':1, '_id':1} -> {'x':1, '_id':1}
    '''
    def update_one(self, coll_name, filter, update, upsert=False):
        try:
            if self._connected:
                return self._db[coll_name].update_one(filter, update, upsert)  
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    Parameters:
        filter: A query that matches the document to update.
        update: The modifications to apply.
        upsert (optional): If True, perform an insert if no documents match the filter.
    Examples:
        db.test.update_one({'x': 1}, {'$inc': {'x': 3}})
        {'x':1, '_id':0} -> {'x':4, '_id':0}
        {'x':1, '_id':1} -> {'x':4, '_id':1}
    '''
    def update_many(self, coll_name, filter, update, upsert=False):
        try:
            if self._connected:
                return self._db[coll_name].update_many(filter, update, upsert)  
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    Parameters:
    Examples:
        db.test.insert_one({'x': 1})
    '''
    def insert_one(self, coll_name, document):
        try:
            if self._connected:
                return self._db[coll_name].insert_one(document)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    Parameters:
        ordered (optional): 
            If True (the default) documents will be inserted on the server serially, in the order provided. If an error occurs all remaining inserts are aborted. 
            If False, documents will be inserted on the server in arbitrary order, possibly in parallel, and all document inserts will be attempted
    '''
    def insert_many(self, coll_name, documents, ordered=True):
        try:
            if self._connected:
                return self._db[coll_name].insert_many(documents, ordered)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    Get a single document from the collection of coll_name
    Parameters:
        filter (optional): a dictionary specifying the query to be performed OR any other type to be used as the value for a query for "_id"
    Examples:
        db.test.find_one(max_time_ms=100)
        db.test.find_one({'x': 1})
    '''
    def find_one(self, coll_name, filter_or_id=None, *args, **kwargs):
        try:
            if self._connected:
                return self._db[coll_name].find_one(filter_or_id, *args, **kwargs)
        except Exception, err:
            log.app_log.error(traceback.format_exc())
        

    '''
    The filter  argument is a prototype document that all results must match. For example:
    db.test.find({"hello": "world"})
    Parameters:
        filter (optional): a SON object specifying elements which must be present for a document to be included in the result set
        projection (optional): a list of field names that should be returned in the result set or a dict specifying the fields to include or exclude.
             If projection is a list “_id” will always be returned. Use a dict to exclude fields from the result (e.g. projection={‘_id’: False}).
        sort: ("_id", pymongo.ASCENDING)
        allow_partial_results (optional): if True, mongos will return partial results if some shards are down instead of returning an error.
    '''
    def find(self, coll_name, filter=None, projection=None, skip=0, limit=0, sort=None, allow_partial_results=False, find_batch_size=0):
        try:
            if self._connected:
                if find_batch_size > 0:
                    return self._db[coll_name].find(filter=filter, projection=projection, skip=skip, limit=limit, sort=sort, allow_partial_results=allow_partial_results).batch_size(find_batch_size)
                else:
                    return self._db[coll_name].find(filter=filter, projection=projection, skip=skip, limit=limit, sort=sort, allow_partial_results=allow_partial_results)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    Finds a single document and updates it, returning either the original or the updated document.
    Parameters:
        filter: A query that matches the document to update
        update: The update operations to apply.
        projection (optional): A list of field names that should be returned in the result document or a mapping specifying the fields to include or exclude. If projection is a list “_id” will always be returned. Use a dict to exclude fields from the result (e.g. projection={‘_id’: False}).
        sort (optional): a list of (key, direction) pairs specifying the sort order for the query. If multiple documents match the query, they are sorted and the first is updated.
        upsert (optional): When True, inserts a new document if no document matches the query. Defaults to False.
        return_document: If ReturnDocument.BEFORE (the default), returns the original document before it was updated, or None if no document matches. If ReturnDocument.AFTER, returns the updated or inserted document.
        **kwargs (optional): additional command arguments can be passed as keyword arguments
    Examples:
        db.example.find_one_and_update({'_id': 'userid'}, {'$inc': {'seq': 1}}, projection={'seq': True, '_id': False}, upsert=True, return_document=ReturnDocument.AFTER)
    '''
    def find_one_and_update(self, coll_name, filter, update, projection=None, sort=None, upsert=False, return_document=0, **kwargs):
        try:
            if self._connected:
                if return_document == 0:
                    return self._db[coll_name].find_one_and_update(filter, update, projection, sort, upsert, ReturnDocument.BEFORE, **kwargs)  
                elif return_document == 1:
                    return self._db[coll_name].find_one_and_update(filter, update, projection, sort, upsert, ReturnDocument.AFTER, **kwargs)  
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    
    def find_one_and_replace(self, filter, replacement, projection=None, sort=None, upsert=False, return_document=0, **kwargs):
        try:
            if self._connected:
                if return_document == 0:
                    return self._db[coll_name].find_one_and_replace(filter, replacement, projection, sort, upsert, ReturnDocument.BEFORE, **kwargs)  
                elif return_document == 1:
                    return self._db[coll_name].find_one_and_replace(filter, replacement, projection, sort, upsert, ReturnDocument.AFTER, **kwargs)  
        except Exception, err:
            log.app_log.error(traceback.format_exc())


    '''
    Finds a single document and deletes it, returning the document
    Parameters:
        filter: A query that matches the document to delete.
        projection (optional): a list of field names that should be returned in the result document or a mapping specifying the fields to include or exclude. If projection is a list “_id” will always be returned. Use a mapping to exclude fields from the result (e.g. projection={‘_id’: False}).
        sort (optional): a list of (key, direction) pairs specifying the sort order for the query. If multiple documents match the query, they are sorted and the first is deleted.
        **kwargs (optional): additional command arguments can be passed as keyword arguments (for example maxTimeMS can be used with recent server versions).
    Examples:
        sort=[('_id', pymongo.DESCENDING)]
    '''
    def find_one_and_delete(self, coll_name, filter, projection=None, sort=None, **kwargs):
        try:
            if self._connected:
                return self._db[coll_name].find_one_and_delete(filter, projection, sort, **kwargs)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    '''
    All optional count parameters should be passed as keyword arguments to this method. Valid options include
    Parameters:
        filter (optional): A query document that selects which documents to count in the collection.
        **kwargs:
            hint (string or list of tuples): The index to use. Specify either the index name as a string or the index specification as a list of tuples (e.g. [(‘a’, pymongo.ASCENDING), (‘b’, pymongo.ASCENDING)]).
            limit (int): The maximum number of documents to count.
            skip (int): The number of matching documents to skip before returning results.
            maxTimeMS (int): The maximum amount of time to allow the count command to run, in milliseconds
    '''
    def count(self, coll_name, filter=None, **kwargs):
        try:
            if self._connected:
                return self._db[coll_name].count(filter, **kwargs)
        except Exception, err:
            log.app_log.error(traceback.format_exc())


    '''
    Parameters:
        key: name of the field for which we want to get the distinct values
        filter (optional): A query document that specifies the documents from which to retrieve the distinct values
        **kwargs (optional): See list of options above.
    '''
    def distinct(self, coll_name, key, filter=None, **kwargs):
        try:
            if self._connected:
                return self._db[coll_name].distinct(key, filter, **kwargs)
        except Exception, err:
            log.app_log.error(traceback.format_exc())


if __name__ == '__main__':
    import time
    import pymongo
    try:
        test = MongoConnect(urls='192.168.16.165:27017', db='xv', user='xv', passwd='xv')
        coll_name = 'msg_history'
        now = int(time.time())
        while True:
            result = test.find_one(coll_name, {"msg_level":1})
            if result:
                print result['msgid']
            time.sleep(2)
    except Exception, err:
        print err
        print traceback.format_exc()
        log.app_log.error(traceback.format_exc())
        time.sleep(2)

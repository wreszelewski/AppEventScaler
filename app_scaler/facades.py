from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine
import json
import boto3
import os

class AppRepoFacade(object):

    def __init__(self, config):

        self.conf = config
        self.s3 = boto3.resource('s3', **self.conf['ec2']['access'])
        for bucket in self.s3.buckets.all():
            print(bucket.name)

    def put(self, path, obj):
        key = os.path.join(self.conf['s3']['path_prefix'], path) 
        s3_obj = self.s3.Object(self.conf['s3']['bucket'],
            key)
        s3_obj.put(Body=obj)

    def get(self, path):
        key = os.path.join(self.conf['s3']['path_prefix'], path)
        obj = self.s3.Object(self.conf['s3']['bucket'],
            key)
        s3_obj = obj.get()
        return s3_obj['Body'].read()

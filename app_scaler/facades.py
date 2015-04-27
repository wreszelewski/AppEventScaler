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


class VManagerFacade(object):

    def __init__(self, config):
        self.conf = config
        self.ec2 = boto3.client('ec2', **self.conf['ec2']['access'])

    def create_vm(self):
        instance = self.ec2.run_instances(**self.conf['ec2']["vm_params"])
        return instance

    def destroy_vm(self, vm_id):
        self.ec2.terminate_instances(InstanceIds=[vm_id])

    def check_vm(self, vm_id):
        status = self.ec2.describe_instances(InstanceIds = [vm_id])['Reservations'][0]['Instances'][0]['State']['Name']
        return status

class StatsFacade(object):

    def __init__(self, config):
        
        self.host = config['stats']['host']
        self.port = config['stats']['port']

        self.http_client = AsyncHTTPClient()

    @coroutine
    def get_stats(self):
        response = yield self.http_client.fetch("http://{}:{}/stats".format(self.host, self.port))
        stats = json.loads(response.body.decode('utf-8'))
        return stats

class AppFacade(object):

    def __init__(self, config):
        
        self.host = config['lb']['host']
        self.port = config['lb']['port']
        self.slots = config['lb']['slots']

        self.http_client = AsyncHTTPClient()

    @coroutine
    def register(self, backend, host, port):
        response = yield self.http_client.fetch("http://{}:{}/register?backend={}&host={}&port={}&instances={}".format(
            self.host,
            self.port,
            backend,
            host,
            port,
            self.slots
        ))

    @coroutine
    def unregister(self, backend, host, port):
        response = yield self.http_client.fetch("http://{}:{}/unregister?backend={}&host={}&port={}".format(
            self.host,
            self.port,
            backend,
            host,
            port
        ))

    def run(self):
        pass

    def stop(self):
        pass



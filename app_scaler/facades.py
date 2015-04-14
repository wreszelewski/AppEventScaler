from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine
import json
import boto3

class AppRepoFacade(object):

    def put(self, obj):
        pass

    def get(self, path):
        return None


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

    def register(self):
        pass

    def unregister(self):
        pass

    def run(self):
        pass

    def stop(self):
        pass



import json

class Config(object):

    def __init__(self, config_path="config.json"):

        with open(config_path, "r") as cfg:
            self.conf = json.load(cfg)

    def __getitem__(self, key):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value

import json
import os

class Config(object):

    def __init__(self, config_path=None):

        if config_path is None:
           config_path = os.path.join("/etc", "aesc_minion.conf")

        with open(config_path, "r") as cfg:
            self.conf = json.load(cfg)

    def __getitem__(self, key):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value

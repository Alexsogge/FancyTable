import xml.etree.ElementTree as ET
import json
import os
from typing import List, Dict, Tuple, Union

config_file = './config.json'

class ConfigAdapter:

    def __init__(self, application_name, default_config: Dict):
        self.application_name = application_name
        print(application_name)
        self.root = None

        self.open_config_file()

        self.config = None
        self.load_config()
        for key in default_config.keys():
            if key not in self.config:
                self.config[key] = default_config[key]
                self.save_config()


    def open_config_file(self):
        if not os.path.isfile(config_file):
            with open(config_file, 'w') as outfile:
                json.dump({}, outfile)

        with open(config_file) as json_file:
            self.root = json.load(json_file)


    def load_config(self):
        if self.application_name in self.root:
            self.config = self.root[self.application_name]
        else:
            self.root[self.application_name] = {}
            self.save_config()
            self.config = self.root[self.application_name]

    def get_value(self, entry):
        return self.config[entry]

    def set_value(self, entry, value):
        self.config[entry] = value
        self.save_config()

    def write_config_values(self, config: Dict):
        self.config = config
        self.save_config()

    def read_saved_values(self) -> Dict:
        return self.config


    def save_config(self):
        with open(config_file, 'w') as outfile:
            json.dump(self.root, outfile)

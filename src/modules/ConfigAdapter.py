import xml.etree.ElementTree as ET
import os
from typing import List, Dict, Tuple, Union


class ConfigAdapter:

    def __init__(self, application_name, default_config: Dict):
        self.application_name = application_name
        print(application_name)

        self.tree = self.open_config_file()
        self.root = self.tree.getroot()
        self.config: ET.Element = self.load_config()
        if len(list(default_config.keys())) > 0:
            if self.get_value(list(default_config.keys())[0]) is None:
                self.write_config_values(default_config)


    def open_config_file(self) -> ET.ElementTree:
        if not os.path.isfile('./config.xml'):
            root = ET.Element('root')
            tree = ET.ElementTree(root)
            tree.write('./config.xml')

        tree = ET.parse('./config.xml')
        return tree

    def load_config(self):
        config = self.root.find(self.application_name)
        print(config)
        if config is None:
            ET.SubElement(self.root, self.application_name)
            self.save_config()
            config = self.root.find(self.application_name)
        return config

    def get_value(self, entry):
        return self.config.get(entry)

    def set_value(self, entry, value):
        self.config.set(entry, str(value))
        self.save_config()

    def write_config_values(self, config: Dict):
        for key, value in config.items():
            self.set_value(key, value)

    def read_saved_values(self) -> Dict:
        config = dict()
        for key, value in self.config.items():
            config[key] = value
        return config


    def save_config(self):
        self.tree.write('./config.xml')

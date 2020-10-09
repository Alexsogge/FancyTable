from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync
from typing import Dict
import json
from os import listdir
from .models import *

config_file = '../src/config.json'

def send_message(content: Dict):
    print("SEND:", content)
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('table', {
        'type': 'message',
        'content': content
    })


def update_config(extension_name, config_key, config_value):
    content = {'action': 'config_update', 'extension_name': extension_name, 'config_key': config_key,
               'config_value': config_value}
    send_message(content)

def switch_ectension(target: Extension):
    print("Switching extension")
    content = {'action': 'switch_extension', 'extension': target.extension_name}
    send_message(content)


def load_saved_config_file():
    print(listdir('../src/'))
    with open(config_file) as json_file:
        root = json.load(json_file)
        for extension_name, config in root.items():
            extension_mod = Extension.objects.filter(extension_name=extension_name)
            if extension_mod.exists():
                extension = extension_mod.first()
            else:
                print("No model")
                extension = Extension.objects.create(extension_name=extension_name)

            for config_key, config_value in config.items():
                config_entry_mod = ConfigEntry.objects.filter(extension=extension)
                if config_entry_mod.exists():
                    config_entry: ConfigEntry = config_entry_mod.first()
                    config_entry.config_value = str(config_value)
                    config_entry.save()
                else:
                    ConfigEntry.objects.create(extension=extension, config_key=config_key, config_value=config_value)




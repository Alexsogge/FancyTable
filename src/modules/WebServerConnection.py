

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import threading
from modules.ConfigAdapter import ConfigAdapter
from modules.ExtensionManager import ExtensionManager
from typing import Union, Dict
from extensiones import Extension

class WebServerConnection(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.config_adapter = ConfigAdapter('WebServerConnection', {})

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://192.168.0.11:80/ws/table/",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open
        print("Started webserver")

        self.running = True
        self.extension_manager: Union[ExtensionManager, None] = None

    def initialize(self, extension_manager: ExtensionManager):
        self.extension_manager = extension_manager

    def run(self):
        self.ws.run_forever()
        print("Webserver running")

    def on_message(self, message):
        print("WS message", message)
        content = json.loads(message)['message']
        action = content['action']
        if action == 'config_update':
            value = content['config_value']
            if type(value) == str:
                if value.lower() == 'true' or value.lower() == 'false':
                    value = value.lower() == 'true'
                try:
                    value = float(value)
                except ValueError:
                    pass
            self.config_adapter.root[content['extension_name']][content['config_key']] = value
            self.config_adapter.save_config()

        if action == 'switch_extension':
            if self.extension_manager is not None:
                self.extension_manager.open_extension(content['extension'])


    def on_error(self, error):
        print("WS erroe:", error)

    def on_close(self):
        print("### closed ###")
        self.running = False

    def on_open(self):
        def run(*args):
            while self.running:
                time.sleep(5)
                # self.ws.send(json.dumps({'message': 'Hello'}))
                # self.running = False
            time.sleep(1)
            self.ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())


    def save_data(self, extension: Extension, field_name: str, content: Dict):
        message = {'action': 'save_data','extension_name': type(extension).__name__, 'field_name': field_name, 'content': content}
        try:
            self.ws.send(json.dumps({'message': message}))
        except Exception:
            print("Webservice error")

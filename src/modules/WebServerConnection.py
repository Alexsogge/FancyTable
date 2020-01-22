

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import threading


class WebServerConnection(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("ws://localhost:8000/ws/table/",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open


        self.running = True

    def run(self):
        self.ws.run_forever()


    def on_message(self, message):
        print("Message:", message)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")
        self.running = False

    def on_open(self):
        def run(*args):
            while self.running:
                time.sleep(5)
                self.ws.send(json.dumps({'message': 'Hello'}))
                # self.running = False
            time.sleep(1)
            self.ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())
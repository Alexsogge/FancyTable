from modules.Framebuffer import Frame
#from modules.OutputEmulation import OutputEmulation
from modules.RenderingEngine import RenderingEngine
#from modules.InputEmulation import InputEmulation
from modules.ExtensionManager import ExtensionManager
from modules.LEDFrameOutput import LEDFrameOutput
from modules.TouchInput import TouchInputManager
from modules.GuiElements import *
from extensiones import *
from modules.Helpers import *
from modules.WebServerConnection import WebServerConnection
import sys
import time


class TableControl:

    def __init__(self, input_device):
        display = (21, 12)
        # buffer = Frame(display[0], display[1], init_random=False)

        # self.output = OutputEmulation(display[0], display[1], 40)
        self.output = LEDFrameOutput(display[0], display[1])

        self.render_engine = RenderingEngine(display[0], display[1], self.output, False)
        self.render_engine.set_tales(True, 50)
        # self.input_device = InputEmulation(self.output)
        self.input_device = TouchInputManager(input_device, 32000, 34000)
        # self.extension_manager = ExtensionManager(self.render_engine)
        # self.input_device = InputEmulation(self.output)
        self.web_server_connection = WebServerConnection()
        self.extension_manager = ExtensionManager(self.render_engine, self.web_server_connection, self.input_device)
        self.web_server_connection.initialize(self.extension_manager)
        self.web_server_connection.connect()
        # self.web_server_connection.start()
        
        self.output.set_brightness(0.7)


        # self.scroll_text = ScrollingText(self.render_engine, 2, 2, 17, "Langer text", 0.1, Colors.WHITE)


    def main_loop(self):
        last_frame = time.time()
        # self.render_engine.clear_buffer()
        while True:
            time_delta = time.time() - last_frame
            last_frame = time.time()
            self.input_device.read_inputs()
            self.input_device.map_inputs_to_screen(self.render_engine)

            #self.sandbox_loop(time_delta)
            self.control_loop(time_delta)

            self.render_engine.upload_buffer()
            # self.web_server_connection.check_connection()


            time.sleep(0.01)


    def sandbox_loop(self, time_delta):
        self.render_engine.clear_buffer()
        self.scroll_text.loop(time_delta)
        self.scroll_text.display()

    def control_loop(self, time_delta):
        self.input_device.read_inputs()
        self.input_device.map_inputs_to_screen(self.render_engine)

        action: Action
        for input in list(self.input_device.get_inputs().values()):
            #  x, y = self.render_engine.map_input(input.x, input.y)
            for action in input.load_actions():
                # render_engine.draw_pixel(action.pixels[0], action.pixels[1], Colors.YELLOW)
                self.extension_manager.process_input(action)
                # print(action)
                if action.type == ActionType.RELEASED:
                    self.input_device.clear_inputs(input.z)
                    break
            # input.clear()

        self.extension_manager.loop(time_delta)




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 TableControl.py <device path>")
        sys.exit(1)


    #web_server_connection = WebServerConnection()
    #web_server_connection.start()
    print("Start application")

    control = TableControl(sys.argv[1])


    control.main_loop()


    #render_engine.draw_circle(10, 7, 7, Colors.RED, True)
    #print("#################################################################")
    #render_engine.draw_line(10, 7, 5, 1, Colors.YELLOW)

    # buffer.set_tales(True, 0.01)

    # output = EmulatedOutput(display[0], display[1])
    # output = LEDFrameOutput(display[0], display[1])
    # buffer.add_output(output)

    # input_manager = TouchInputManager(sys.argv[1])
    # input_manager.define_display(display[0], display[1])
    # input_manager.calibrate(buffer)


#    input_manager.load_calibration(32000, 34000)

    #buffer.set_pixel(5, 4, 5, 0, 0)

    #pixel = [0, 0]

#    buffer.upload_frame()






from modules.Framebuffer import Frame
from modules.OutputEmulation import OutputEmulation
from modules.RenderingEngine import RenderingEngine
from modules.InputEmulation import InputEmulation
from modules.ExtensionManager import ExtensionManager
from extensiones import *
from modules.Helpers import *
import sys
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 TableControl.py <device path>")
        sys.exit(1)

    display = (30, 15)
    # buffer = Frame(display[0], display[1], init_random=False)

    output = OutputEmulation(display[0], display[1], 40)

    render_engine = RenderingEngine(display[0], display[1], output, False)
    render_engine.set_tales(True, 50)

    input_device = InputEmulation(output)

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

    extension_manager = ExtensionManager(render_engine)


#    input_manager.load_calibration(32000, 34000)

    #buffer.set_pixel(5, 4, 5, 0, 0)

    #pixel = [0, 0]

#    buffer.upload_frame()

    counter = 0
    r = 1
    direction = 1

    print("Start")
    while True:
        input_device.read_inputs()
        input_device.map_inputs_to_screen(render_engine)

        action: Action
        for input in input_device.get_inputs().values():
            x, y = render_engine.map_input(input.x, input.y)
            for action in input.actions:
                # render_engine.draw_pixel(action.pixels[0], action.pixels[1], Colors.YELLOW)
                extension_manager.process_input(action)
                if action.type == ActionType.RELEASED:
                    input_device.clear_inputs()
                    break

        extension_manager.loop(0)

#         if counter > 2:
#             render_engine.clear_buffer()
#             render_engine.draw_circle(20, 10, r, Colors.RED, False)
#             r += direction
#             if r > 10:
#                 direction = -1
#             if r < 2:
#                 direction = 1
#             counter = 0
#         counter += 1

        # render_engine.clear_buffer()
#        input_manager.read_inputs()
#        # print(input_manager.get_inputs().items())
#        for slot, tinput in input_manager.get_inputs().items():
#            input_states = tinput.get_states()
#            while not input_states.empty():
#                input_action = input_states.get()
#                input_action.add_pixels(input_manager.map_to_display(input_action.x, input_action.y))
#                extension_manager.process_input(slot, input_action)
#                # state = input_states.get()
#                # draw(state.x, state.y, slot)
#        #buffer.clear_frame()
#        extension_manager.loop()
#        buffer.upload_frame()
        render_engine.upload_buffer()
        time.sleep(0.01)

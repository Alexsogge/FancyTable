from modules import *
from extensiones import *
import sys
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 TableControl.py <device path>")
        sys.exit(1)

    display = (21, 12)
    buffer = Frame(display[0], display[1], init_random=False)
    # buffer.set_tales(True, 0.01)

    # output = EmulatedOutput(display[0], display[1])
    output = LEDFrameOutput(display[0], display[1])
    buffer.add_output(output)

    input_manager = TouchInputManager(sys.argv[1])
    input_manager.define_display(display[0], display[1])
    # input_manager.calibrate(buffer)

    extension_manager = ExtensionManager(buffer)


    input_manager.load_calibration(34000, 34000)

    #buffer.set_pixel(5, 4, 5, 0, 0)

    #pixel = [0, 0]

    buffer.upload_frame()



    while True:
        input_manager.read_inputs()
        # print(input_manager.get_inputs().items())
        for slot, tinput in input_manager.get_inputs().items():
            input_states = tinput.get_states()
            while not input_states.empty():
                input_action = input_states.get()
                input_action.add_pixels(input_manager.map_to_display(input_action.x, input_action.y))
                extension_manager.process_input(slot, input_action)
                # state = input_states.get()
                # draw(state.x, state.y, slot)
        #buffer.clear_frame()
        extension_manager.loop()
        buffer.upload_frame()
        time.sleep(0.01)

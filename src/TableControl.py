from modules import *
import sys




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 TableControl.py <device path>")
        sys.exit(1)

    display = (22, 10)
    buffer = Frame(display[0], display[1])
    buffer.set_tales(True, 0.01)

    output = EmulatedOutput(display[0], display[1])
    buffer.add_output(output)

    input_manager = TouchInputManager(sys.argv[1])
    input_manager.define_display(display[0], display[1])
    input_manager.calibrate(buffer)
    #input_manager.load_calibration(28000, 25000)

    buffer.set_pixel(5, 4, 5, 0, 0)

    pixel = [0, 0]

    buffer.upload_frame()

    def draw(x, y, color):
        dx, dy = input_manager.map_to_display(x, y)
        #print("Draw to: ", dx,dy)
        buffer.set_pixel(dx, dy, int(color)+7, 0, 0)



    while True:
        input_manager.read_inputs()
        #print(input_manager.get_inputs().items())
        for slot, tinput in input_manager.get_inputs().items():
            input_states = tinput.get_states()
            while True:
                if input_states.empty():
                    break
                state = input_states.get()
                draw(state.x, state.y, slot)
        buffer.clear_frame()
        buffer.upload_frame()



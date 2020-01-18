from .InputDevice import *
from .OutputEmulation import OutputEmulation
from .Helpers import *


class InputEmulation(InputDevice):

    def __init__(self, emulated_output):
        super().__init__()
        self.emulated_output: OutputEmulation = emulated_output
        self.width = emulated_output.width
        self.height = emulated_output.height
        self.last_pos = None
        self.mouse_up = True
        self.release_back_keys = False


    def read_inputs(self):
        event, values = self.emulated_output.window.Read(10)

        # print((event), (values))

        if event == 'Left:113':
            self.new_input(self.width * 0.2, self.height*0.95, 1)
            self.inputs[1].press()
            self.inputs[1].release()

        if event == 'Right:114':
            self.new_input(self.width * 0.8, self.height*0.95, 1)
            self.inputs[1].press()
            self.inputs[1].release()

        if self.release_back_keys:
            self.inputs[2].release()
            self.inputs[3].release()
            self.inputs[4].release()
            self.release_back_keys = False

        if event == '':
            self.new_input(self.width * 0.5, 5, 2)
            self.inputs[2].press()
            self.inputs[2].move(0.5, 0.98)

            self.new_input(self.width * 0.5, 5, 3)
            self.inputs[3].press()
            self.inputs[3].move(0.5, 0.98)

            self.new_input(self.width * 0.5, 5, 4)
            self.inputs[4].press()
            self.inputs[4].move(0.5, 0.98)

            self.release_back_keys = True


        new_action = None
        pos = values['graph']
        if pos[1] is not None:
            pos = (pos[0], self.height - pos[1])

        if event == '__TIMEOUT__':
            if pos[0] is not None:
                if self.last_pos is None:
                    self.mouse_up = False
                    self.new_input(pos[0], pos[1], 0)
                    self.inputs[0].press()
                else:
                    if self.mouse_up is False or self.last_pos[0] != pos[0] or self.last_pos[1] != pos[1]:
                        if 0 in self.inputs:
                            self.inputs[0].release()
                            self.last_pos = pos
                            self.mouse_up = True
                        else:
                            self.new_input(pos[0], pos[1], 0)
                            self.inputs[0].press()
                            self.mouse_up = False
                self.last_pos = pos

        if event == 'graph':
            if pos[0] is not None:
                if self.last_pos is None or (self.last_pos[0] != pos[0] or self.last_pos[1] != pos[1]):
                    if 0 not in self.inputs:
                        self.new_input(pos[0], pos[1], 0)
                    if self.last_pos is not None:
                        print((self.last_pos[0] != pos[0] or self.last_pos[1] != pos[1]))
                    self.inputs[0].move(self.u(pos[0]), self.v(pos[1]))
                self.last_pos = pos

        if event == 'graph+UP':
            if 0 in self.inputs:
                self.inputs[0].release()
                self.last_pos = pos
                self.mouse_up = True










import time
from neopixel import *
import argparse

class LEDFrameOutput:

    # LED strip configuration:
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


    width = 0
    height = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.strip = Adafruit_NeoPixel(width*height, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
                                  self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()


    def upload(self, frame_matrix):
        for y, row in enumerate(frame_matrix):
            for x, col in enumerate(row):
                pix = frame_matrix[x][y]
                if y % 2 == 0:
                    x = len(row) - x
                self.strip.setPixelColorRGB(y*x, pix['r'], pix['g'], pix['b'])
        self.strip.show()


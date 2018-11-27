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

    dimming = 0.003

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.strip = Adafruit_NeoPixel(width*height+1, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,
                                  self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()


    def upload(self, frame_matrix):
        max_led = self.width * self.height
        for y, row in enumerate(frame_matrix):
            for x, col in enumerate(row):
                pix = col
                if y % 2 == 1:
                    x = len(row) - 1 - x
                led_num = (self.height - 1 - y) * self.width + x
                R, G, B = max(min(int(255 * pix['r'] * self.dimming), 255), 0), max(min(int(255 * pix['g'] * self.dimming), 255), 0), \
                          max(min(int(255 * pix['b'] * self.dimming), 255), 0)
                self.strip.setPixelColorRGB(led_num, R, G, B)
                # print("Write on", led_num, pix)
        self.strip.show()

    def inc_dimming(self, val):
        self.dimming += val
        self.dimming = max(min(self.dimming, 1), 0)


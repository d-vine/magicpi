import  RPi.GPIO as GPIO
import time
import sys
import cursor
from neopixel import *
from termcolor import colored, cprint

# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 21      # GPIO pin connected to the pixels (21 uses PCM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

cursor.hide()

GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_UP)

changed = False
size = 4
position = 0
oldColorName = ''
delay = 0
maxDelay = 1
colors = ['grey'for x in range(size)]
newColor = Color(0,0,0)

def getColorName(red, green, blue, reset):
    if (reset): return 'reset'
    if (red and green and blue): return 'white'
    if (red and green): return 'yellow'
    if (red and blue): return 'magenta'
    if (blue and green): return 'cyan'
    if (red): return 'red'
    if (blue): return 'blue'
    if (green): return 'green'
    return 'grey'

def getColor(red, green, blue, reset):
    if (reset): return Color(0,0,0)
    redVal = 255 if red else 0
    greenVal = 255 if green else 0
    blueVal = 255 if blue else 0
    return Color(greenVal, redVal, blueVal)


def makeLight(color, active):
    text = '  X  ' if active else '     '
    return colored(text,'grey','on_%s' % color)

def resetColors():
    global colors, position
    colors = ['grey'for x in range(size)]
    position = 0
    strip.setPixelColor(0, Color(0,0,0))
    strip.show()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
# Intialize the library (must be called once before other functions).
strip.begin()

print "READY"

while True:
    reset = not GPIO.input(26)
    blue = not GPIO.input(17)
    green = not GPIO.input(27)
    red = not GPIO.input(22)
    newColorName = getColorName(red, green, blue, reset)
    if (newColorName != oldColorName):
        newColor = getColor(red, green, blue, reset)
        oldColorName = newColorName
        delay = 0
        time.sleep(0.1)
    else:
        if (delay <= maxDelay):
            if (delay == maxDelay):

                if (newColorName == 'grey'):
                    if (changed):
                        position = (position + 1) % size
                        changed = False
                elif (newColorName == 'reset'):
                    colors[position] = 'grey'
                    strip.setPixelColor(0, Color(0,0,0))
                    strip.show()
                    changed = False
                    position = (position + 1) % size
                    # resetColors()
                else:
                    colors[position] = newColorName
                    strip.setPixelColor(0, newColor)
                    strip.show()
                    changed = True
                sys.stdout.write("\r" + ''.join([makeLight(colors[i], i == position) for i in range(size)]))
                sys.stdout.flush()
            delay += 1
            time.sleep(0.1)

import  RPi.GPIO as GPIO
import time
import sys
import cursor
from termcolor import colored, cprint

cursor.hide()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_UP)

changed = False
size = 4
position = 0
oldColor = ''
delay = 0
maxDelay = 1
colors = ['grey'for x in range(size)]

def getColor(red, green, blue, reset):
    if (reset): return 'reset'
    if (red and green and blue): return 'white'
    if (red and green): return 'yellow'
    if (red and blue): return 'magenta'
    if (blue and green): return 'cyan'
    if (red): return 'red'
    if (blue): return 'blue'
    if (green): return 'green'
    return 'grey'

def makeLight(color, active):
    text = '  X  ' if active else '     '
    return colored(text,'grey','on_%s' % color)

def resetColors():
    global colors, position
    colors = ['grey'for x in range(size)]
    position = 0


while True:
    reset = not GPIO.input(26)
    blue = not GPIO.input(17)
    green = not GPIO.input(27)
    red = not GPIO.input(22)
    newColor = getColor(red, green, blue, reset)
    if (newColor != oldColor):
        oldColor = newColor
        delay = 0
        time.sleep(0.1)
    else:
        if (delay <= maxDelay):
            if (delay == maxDelay):

                if (newColor == 'grey'):
                    if (changed):
                        position = (position + 1) % size
                        changed = False
                elif (newColor == 'reset'):
                    resetColors()
                else:
                    colors[position] = newColor
                    changed = True
                sys.stdout.write("\r" + ''.join([makeLight(colors[i], i == position) for i in range(size)]))
                sys.stdout.flush()
            delay += 1
            time.sleep(0.1)

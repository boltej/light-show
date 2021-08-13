import machine
from ws2812 import WS2812
from machine import Pin
import utime
from utime import sleep
import urandom

 #import rgb_colors

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
white = (255,255,255)
blank = (0,0,0)

color_array = [red, green, blue, yellow, cyan]

#Set up variables for configuration

n = 8 #number of LEDs
p = 0 #Pin Number (needs to be ADC)
#b = .5 #default brightness

ws = WS2812(machine.Pin(p),n)
#ws[0] = red
#ws.write()

#Functions
def ind_glow(): #Causes a single LED to glow from dark to light and back.
    for i in range (0, 1000):
        print(i)
        ws = WS2812(machine.Pin(p),n, i/1000)
        ws[0] = red
        ws.write()
    for i in range (1000, 0, -1):
        ws = WS2812(machine.Pin(p),n, i/1000)
        ws[0] = red
        ws.write()
        
def all_glow(): #Causes all LEDs to glow from dark to light and back
    for num in range(1, n):
        for i in range (0, 500):
            print(i)
            ws = WS2812(machine.Pin(p),n, i/500)
            ws[num] = red
            ws.write()
        for i in range (500, 0, -1):
            ws = WS2812(machine.Pin(p),n, i/500)
            ws[num] = red
            ws.write()

def sound_glow(): # Causes all LEDs to glow based on the amount of sound the microphone picks up.
                  # If the sound does not make it above a certain threshold, then the LEDs stay blank
    #ws = WS2812(machine.Pin(p),n)
    global scale, min_signal, active
    random_color = color_array[urandom.randint(0, (len(color_array) - 1))]
    max_signal = 0
    for j in range(0, 1024):
        signal = sound_sensor.read_u16()
        if signal > max_signal:
            max_signal = signal
        if signal < min_signal:
            min_signal = signal
    #i = max(signal/1024)
    #i = ((max_signal * cf) / 21844) #for microphone values
    if max_signal > scale:
            scale = max_signal
    i = max_signal / (scale - min_signal)
    #print(i, max_signal)
    if i > .18:
        #ws.write_all(int(urandom.uniform(0, 0xFFFFFF)))
        ws.brightness = i/5
        ws.write_all(random_color)
        #utime.sleep_ms(75)
        active = True
    else:
        if active == True:
            for b in range(int(i*100), 0, -1):
                ws.brightness = b/100
                print(b/100)
                ws.write_all(random_color)
                utime.sleep_ms(5)
            active = False
        ws.write_all(blank)
            
sound_sensor = machine.ADC(26) #sets up the sound sensor to pick up analog input from microphone.
min_signal = 800
#reading = sound_sensor.read_u16() * cf
scale = 8000
active = False

#ws.brightness = .1
#ws[0] = red
#ws.write()

ws = WS2812(machine.Pin(p),n)

while True:å
    sound_glow()
    #utime.sleep_ms(100)


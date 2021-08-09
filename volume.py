import machine
from ws2812 import WS2812
import utime
#import rgb_colors

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
white = (255,255,255)
blank = (0,0,0)

ws = WS2812(machine.Pin(0),8)
#ws.Lightning(red)
#ws.Loop((128,10,233),(0,0,0),20)
#ws.Breathe(red)
#ws.Breathe(green)
#ws.Breathe(blue)
#ws.Blank()

# read the guitar output on pin 28
# This configures pin GP28_ADC2 as the first channel, ADC2, on the analogue-to-digital converter.
jack = machine.ADC(28)

minSignal = 600
maxSignal = minSignal+1

#To read from the pin, set up a loop:
while True:
    #print(jack.read_u16())
    signal = jack.read_u16()
    
    if signal > maxSignal:
        maxSignal = signal
        
    if signal <= minSignal:
        ws.Blank()
    else:
        s = (signal-minSignal)/(maxSignal-minSignal)
        ws.brightness = s
        ws.Flash(red,0.15)
        print(s)
        
    utime.sleep(0.02)
    

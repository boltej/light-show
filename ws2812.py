import array, time
import random
#import rp2
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]
    
class WS2812():

    def __init__(self, pin, num):
        # Configure the number of WS2812 LEDs.
        self.ledCount = num
        self.pin = pin
        self.brightness = 1.0
        self.sm = StateMachine(0, ws2812, freq=8000000, sideset_base=self.pin)
        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)

        self.pixelArray = array.array("I", [0 for _ in range(self.ledCount)])
        self.brightnessArray = array.array("I", [1 for _ in range(self.ledCount)])

    def write(self):
        self.sm.put(self.pixelArray, 8)

    def write_all(self, value):
        for i in range(self.ledCount):
            self.__setitem__(i, value)
        self.write()

    def rgb_to_hex(self, color):
        if (isinstance(color, list) or isinstance(color,tuple)) and len(color) == 3:
            #r = int(((color[0] >> 8) & 0xFF) * self.brightness) # 8-bit red dimmed to brightness
            #g = int(((color[1] >> 16) & 0xFF) * self.brightness) # 8-bit green dimmed to brightness
            #b = int((color[2] & 0xFF) * self.brightness) # 8-b            c = (color[0] << 8) + (color[1] << 16) + (color[2])
            #c = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
            
            r = int(color[0]*self.brightness)
            g = int(color[1]*self.brightness)
            b = int(color[2]*self.brightness)
            
            c = (r << 8) + (g << 16) + (b)
            return c
        elif isinstance(color, int):
            value = (color & 0xFF0000)>>8 | (color & 0x00FF00)<<8 | (color & 0x0000FF)
            return value
        else:
            raise ValueError("Color must be 24-bit  RGB hex or list of 3 8-bit RGB")

    def hex_to_rgb(self, color):
        if isinstance(color, list) and len(color) == 3:
            return color
        elif isinstance(color, int):
            r = color >> 8 & 0xFF
            g = color >> 16 & 0xFF
            b = color >> 0 & 0xFF
            return (r, g, b)
        else:
            raise ValueError("Color must be 24-bit  RGB hex or list of 3 8-bit RGB")

    def __getitem__(self, i):
        return self.hex_to_rgb(self.pixelArray[i])

    def __setitem__(self, i, value):
        #color = self.rgb_to_hex(value[0:3])
        #brightness = value[3] 
        #self.pixelArray[i] = int(color)
        self.pixelArray[i] = self.rgb_to_hex(value)

    def Blank(self):
        for i in range(0,self.ledCount):
            self[i] = (0,0,0)
        self.write()

    def Flash(self,color,duration=1,cycles=1):
        for cycles in range(0,cycles):
            for i in range(self.ledCount):
                self[i] = color
            self.write()
            time.sleep(duration) # wait
            self.Blank()
        
    def Loop(self,color,blank=(0,0,0),cycles=1):
        for ii in range(int(cycles*self.ledCount)+1):
            for jj in range(self.ledCount):
                if jj==int(ii%self.ledCount): # in case we go over number of pixels in array
                    self[jj] = color # color and loop a single pixel
                else:
                    self[jj] = blank # turn others off
            self.write() # update pixel colors
            time.sleep(0.05) # wait 50ms

    def Breathe(self, color):        
        step = 5
        breath_amps = [ii for ii in range(0,255,step)]
        breath_amps.extend([ii for ii in range(255,-1,-step)])
        for ii in breath_amps:
            for jj in range(self.ledCount):
                self[jj] = color # show all colors
            self.brightness = ii/255
            self.write()
            time.sleep(0.02)
    
    def Lightning(self, color):
        # start with a strike, followed by a flash
        for i in range(self.ledCount):
            self[i] = color # show all colors
            self.brightness = 1
            self.write()
            time.sleep(0.05)
        
        # flash        
        time.sleep(1)
        self.Blank()
        time.sleep(0.1)
        for i in range(5):  # five flashes
            for j in range(self.ledCount):
                self[j] = color
            self.write()
          
            flash = random.uniform(0,0.1)
            time.sleep(flash)
            self.Blank()
            flash = random.uniform(0,0.1)
            time.sleep(flash)
        
        self.Blank()       
            
            
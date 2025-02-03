import machine
import utime
from ws2812 import WS2812

ring = WS2812(machine.Pin(15), 12)

mic = machine.ADC(26)

last_palm = 0
one_palm = False
two_palms = False

ambient_noise = sum(mic.read_u16() for _ in range(100)) / 100

while 1:
    
    if last_palm == 0:
        last_palm = utime.ticks_ms()
        
    if (mic.read_u16() > ambient_noise * 1.8):
        
        print("One palm")
        
        if (utime.ticks_ms() - last_palm < 400):
            
            print("Two palms")
            two_palms = True
        
        else:
            one_palm = True
        
        last_palm = utime.ticks_ms()
            
    if (one_palm == True):
        ring.write_all(0x000000)
        one_palm = False
        utime.sleep(0.1)
        
    elif (two_palms == True):
        ring.write_all(0x800080)
        two_palms = False
        one_palm = False
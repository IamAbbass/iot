import time
import board
import busio
#import adafruit_ads1x15.ads1015 as ADS
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS object
#ads = ADS.ADS1015(i2c)
ads = ADS.ADS1115(i2c)

# Create a sinlge ended channel on Pin 0
#   Max counts for ADS1015 = 2047
#                  ADS1115 = 32767
chan = AnalogIn(ads, ADS.P0)

# The ADS1015 and ADS1115 both have the same gain options.
#
#       GAIN    RANGE (V)
#       ----    ---------
#        2/3    +/- 6.144
#          1    +/- 4.096
#          2    +/- 2.048
#          4    +/- 1.024
#          8    +/- 0.512
#         16    +/- 0.256
#
print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    ads.gain = 2/3
    offset   = 0.80
    slope    = 3.5
    
    print('{:5} {:5.3f}'.format(chan.value, chan.voltage*slope+offset))
    #print(pHValue)
    time.sleep(1.5)
import os
import glob
import RPi.GPIO as GPIO # import RPi.GPIO module
import time

#Room 28-01131f661eb4
#Fin  28-01131bcbc56e

#Set Temperature
default_room_temp = 5.0
default_fin_temp  = 1.0


#Setup GPIO
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
GPIO.setwarnings(False) # Disable GPIO Warnings
GPIO.setup(2, GPIO.OUT) # set a port/pin as an output
GPIO.output(2, 1)       # Default Off
 
#Read Folder/Files
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

#Room Sensor SNO.
room_folder = glob.glob(base_dir + '28-01131f661eb4')[0]
room_file   = room_folder + '/w1_slave'

#Fin Sensor SNO.
fin_folder = glob.glob(base_dir + '28-01131bcbc56e')[0]
fin_file   = fin_folder + '/w1_slave'
 
#Get Raw Data Room/Fin
def read_room_temp_raw():
    f = open(room_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_fin_temp_raw():
    f = open(fin_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
#Room Sensor Begin
def read_room_temp():
    lines = read_room_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_room_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
#Room Sensor End
    
    
    
#Fin Sensor Begin 
def read_fin_temp():
    lines = read_fin_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_fin_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
#Fin Sensor Begin


while True:
    #If the room temperature reaches the set value, the HEATER will stop running.
    #Your A/C Temperature sensor will cool down and shut the compressor off.
    
    #If the fins of your A/C are reaching the freezing set point (33F/0.5C factory default), the HEATER will stop running.
    #Your A/C Temperature sensor will cool down and shut the compressor off to allow for a defrost cycle.
    if read_room_temp() <= default_room_temp or read_fin_temp() <= default_fin_temp:
        GPIO.output(2, 1) #Turn Off Heater
        
    elif read_room_temp() >= default_room_temp or read_fin_temp() >= default_fin_temp:
        GPIO.output(2, 0) #Turn On Heater
        
    print('Room Sensor:' + str(read_room_temp()) + '  Fin Sensor:' + str(read_fin_temp()))
    
    
    #GPIO.cleanup()    
    #break
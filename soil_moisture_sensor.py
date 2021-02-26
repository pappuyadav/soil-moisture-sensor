from datetime import datetime
import csv
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def readadc(adcnum,clockpin,mosipin,misopin,cspin):
    if ((adcnum>7) or (adcnum<0)):
        return -1
    GPIO.output(cspin,True)
    GPIO.output(clockpin,False)
    GPIO.output(cspin,False)
    a=adcnum
    a|=0x18
    a<<=3
    for i in range(5):
        if(a&0x80):
            GPIO.output(mosipin,True)
        else:
            GPIO.output(mosipin,False)
        a<<=1
        GPIO.output(clockpin,True)
        GPIO.output(clockpin,False)
    adcout=0
    for i in range(12):
        GPIO.output(clockpin,True)
        GPIO.output(clockpin,False)
        adcout<<=1
        if(GPIO.input(misopin)):
            adcout|= 0x1
    GPIO.output(cspin,True)
    adcout>>=1
    return adcout

def convertvoltage(bitvalue,decimalplaces=2):
    voltage=(bitvalue*3.3)/float(1023)
    voltage=round(voltage,decimalplaces)
    return voltage

clk=18
miso=23
mosi=24
chipselect=25

GPIO.setup(mosi,GPIO.OUT)
GPIO.setup(miso,GPIO.IN)
GPIO.setup(clk,GPIO.OUT)
GPIO.setup(chipselect,GPIO.OUT)

channelnum=0
sleeptime=1
c=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

while True:
    rawdata=readadc(channelnum,clk,mosi,miso,chipselect)
    actualdata=convertvoltage(rawdata)
    vwc=(actualdata-0.5)/0.98
    vwc=round(vwc,2)
    print('vwc=',vwc)
    with open('analogsensordata.csv','a') as f:
              writer=csv.writer(f)
              writer.writerow([c,vwc])
              f.close()
    sleep(sleeptime)

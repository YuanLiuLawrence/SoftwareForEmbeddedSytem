import ubinascii
import network
import machine
import urequests
import usocket
import utime
import esp32
from machine import Pin, Timer, TouchPad
from ntptime import settime
from time import sleep

#Connect to the wifi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
    sta_if.connect('esp32', '12345678')
    while not sta_if.isconnected():
        sleep(1)
    print("Oh Yes! Get connected")
    print("Connected to ")
    print("MAC Address: {0}".format(ubinascii.hexlify(sta_if.config('mac'),':').decode()))
    print("IP Address: {0}".format(sta_if.ifconfig()[0]))

#Interrupt toggle
read = 0
def toggle_read(pin):
    global read
    read = 1
    #Clinet setup

    #response = urequests.get()


#Timer initialization
tim = Timer(1)   
tim.init(period=10000, mode=1, callback=toggle_read)

#Final Loop
while True:
    if read:
        print("HALL: {}".format(esp32.hall_sensor()))
        print("TEMP: {}".format(esp32.raw_temperature()))
        s = usocket.socket()
        addr = usocket.getaddrinfo('api.thingspeak.com',80)[0][-1]
        s.connect(addr)
        #api = 'ZFPT8WK40VQZT2XU'
        s.send('GET https://api.thingspeak.com/update?api_key=ZFPT8WK40VQZT2XU&field1={0}&field2={1} HTTP/1.0\r\n\r\n'.format(esp32.raw_temperature(),esp32.hall_sensor()))
    #s.write('GET '+ 'http://api.thingspeak.com/update?api_key={2}&field2={0}&field1={1}'.format(esp32.hall_sensor(), esp32.raw_temperature(), api)+" HTTP/1.0\r\n\r\n")
    #s.recv(1024)
        s.close()
        read = 0
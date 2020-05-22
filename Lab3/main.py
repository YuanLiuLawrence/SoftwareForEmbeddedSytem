import ubinascii
import network
import machine
import utime
import esp32
from machine import Pin, Timer, TouchPad
from ntptime import settime
from time import sleep

#2.2.4.1
if machine.wake_reason() == machine.TIMER_WAKE:
    print('\nWoke up due to a TIMER_WAKE\n')
elif machine.wake_reason() == machine.TOUCHPAD_WAKE:
    print('\nWoke up due to a TOUCHPAD_WAKE\n')
elif machine.wake_reason() == machine.EXT1_WAKE:
    print('\nWoke up due to a EXT1_WAKE\n')    
    
def p_time(datetime): 
    print("Date: {0:02d}/{1:02d}/{2}".format(datetime[1], datetime[2], datetime[0]))
    print("Time: {0:02d}:{1:02d}:{2:02d} HRS\n".format(datetime[3] - 4, datetime[4], datetime[5]))       

#2.2.1
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
    sta_if.connect('LAWRENCE', '11111111')
    while not sta_if.isconnected():
        sleep(1)
    print("Oh Yes! Get connected")
    print("Connected to LAWRENCE")
    print("MAC Address: {0}".format(ubinascii.hexlify(sta_if.config('mac'),':').decode()))
    print("IP Address: {0}".format(sta_if.ifconfig()[0]))
    
#2.2.2
settime()
tim = Timer(1)
tim.init(period=15000, mode=1, callback=lambda t:p_time(utime.localtime()))

#2.2.3
t1 = TouchPad(Pin(14))
t2 = TouchPad(Pin(32))
t1.config(100)

t2.config(100)
g_led = Pin(33, Pin.OUT)
g_tog = 0
g_led.value(0)

#Toggle the green pin when t2 is touched
def toggle_g(pin):
    global g_tog
    if t2.read() < 100:
        g_tog = 1
    else:
        g_tog = 0
        
tim2 = Timer(2)
tim2.init(period=10, mode=1, callback=toggle_g)

#2.2.4
r_led = Pin(27, Pin.OUT)
p1 = Pin(34, Pin.IN, Pin.PULL_DOWN)
p2 = Pin(39, Pin.IN, Pin.PULL_DOWN)

#When the board is awake, the red led is on
r_led.value(1)

slp = 0
#Make the board to sleep every 30s
def toggle_slp(pin):
    global slp
    slp = 1
        
tim3 = Timer(3)
tim3.init(period=30000, mode=1, callback=toggle_slp)

#Final loop
while True:
    g_led.value(g_tog)
    if (slp):
        print("I am awake. Going to sleep for 1 minute")
        t2.config(0) #Disable t2
        esp32.wake_on_ext1((p1,p2),esp32.WAKEUP_ANY_HIGH) #Wake up due to push botton
        esp32.wake_on_touch(True) #Wake up due to touch pad
        machine.deepsleep(60000)

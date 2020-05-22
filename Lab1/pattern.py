from machine import Pin
from time import sleep

switch1 = Pin(27, Pin.IN, Pin.PULL_DOWN)
switch2 = Pin(33, Pin.IN, Pin.PULL_DOWN)
ct_sw1 = 0
ct_sw2 = 0
cur1 = 0
cur2 = 0
led_R = Pin(15, Pin.OUT)
led_G = Pin(32, Pin.OUT)
led_R.value(0)
led_G.value(0)


while ct_sw1 < 10 and ct_sw2 < 10:
    #Counting press times for sw1
    if cur1 != switch1.value() and cur1 == 1:
        ct_sw1 = ct_sw1 + 1
    cur1 = switch1.value()
    if switch1.value():
        led_R.value(1)
    else:
        led_R.value(0)
    
    #Counting press times for sw2
    if cur2 != switch2.value() and cur2 == 1:
        ct_sw2 = ct_sw2 + 1
    cur2 = switch2.value()
    if switch2.value():
        led_G.value(1)
    else:
        led_G.value(0)
    
    if switch1.value() and switch2.value():      
        led_R.value(0)
        led_G.value(0)
    sleep(0.5)

#After ten times press
if ct_sw1 == 10:    
    while (switch2.value() != 1):
        led_R.value(led_G.value())
        led_G.value(not led_R.value())
        sleep(0.5)

if ct_sw2 == 10:
    while (switch1.value() != 1):
        led_R.value(led_G.value())
        led_G.value(not led_R.value())
        sleep(0.5)

#Complete
led_R.value(0)
led_G.value(0)
print("You have successfully implemented LAB1 DEMO!!!")

    

import ubinascii
import network
import machine
import urequests
import socket
import utime
import esp32
from machine import Pin, Timer, TouchPad
from ntptime import settime
from time import sleep

# Global variables
#TEMP  # measure temperature sensor data
#HALL  # measure hall sensor data
#RED_LED_STATE # string, check state of red led, ON or OFF
#GREEN_LED_STATE # string, check state of red led, ON or OFF
    
def web_page(hall,temp,red_led_state,green_led_state):
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    TEMP, HALL, RED_LED_STATE, GREEN_LED_STAT
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h2>ESP32 WEB Server</h2>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p><a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + green_led_state + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p><a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage

#Connect to the wifi
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

g_led = Pin(33, Pin.OUT)
r_led = Pin(27, Pin.OUT)

#Clinet setup
s = socket.socket()
addr = socket.getaddrinfo(sta_if.ifconfig()[0],80)[0][-1]
s.bind(addr)
s.listen(1)

while True:
    #Initialize variable  
    hall = esp32.hall_sensor()
    temp = esp32.raw_temperature()
    
    if (r_led.value() == 1):
        red_led_state = "ON"
    else:
        red_led_state = "OFF"
    if (g_led.value() == 1):
        green_led_state = "ON"
    else:
        green_led_state = "OFF"

    cl, addr = s.accept()
    read = cl.recv(1024)
    

    if str("favicon.ico") in read:
        pass
    else:
        if str("green_led=on HT") in read:
            g_led.value(1)
            green_led_state = "ON"
        elif str("green_led=off HT") in read:
            g_led.value(0)
            green_led_state = "OFF"
        if str("red_led=on HT") in read:
            r_led.value(1)
            red_led_state = "ON"
        elif str("red_led=off HT") in read:
            r_led.value(0)
            red_led_state = "OFF"
    web = web_page(hall,temp,red_led_state,green_led_state)
    cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n' + web)
    cl.close()
import machine
from machine import Pin
from machine import RTC
from machine import ADC
from machine import PWM
from machine import Timer
from time import sleep

year = input("Year? ")
month = input("Month? ")
day = input("Day? ")
weekday = input("Weekday? ")
hour = input("Hour? ")
minute = input("Minute? ")
second = input("Second? ")
microsecond = input("Microsecond? ")

sw = Pin(27, Pin.IN, Pin.PULL_DOWN)
adc = ADC(Pin(32)) 
adc.atten(adc.ATTN_11DB)
adc.width(adc.WIDTH_9BIT)
led = Pin(14, Pin.OUT)
pwm_r = PWM(Pin(14), freq=10, duty=256)      # create PWM object from a pin
pwm_g = PWM(Pin(12), freq=10, duty=256)      # create PWM object from a pin

interruptf = 0

def p_time(datetime): 
    print("Date: {0:02d}.{1:02d}.{2}".format(datetime[1], datetime[2], datetime[0]))
    print("Time: {0:02d}:{1:02d}:{2:02d}\n".format(datetime[4], datetime[5], datetime[6]))

# def c_freq(pin):
#     #led.value(not led.value())
#     
#     print(led.value())
    
def call(pin):
    global interruptf
    interruptf = interruptf + 1

def cancel_de(pin):
    tim2.init(period=100, mode=Timer.ONE_SHOT, callback=call)
    
rtc = machine.RTC()
rtc.datetime((int(year), int(month), int(day), int(weekday), int(hour), int(minute), int(second), int(microsecond)))
tim = Timer(1)
tim.init(period=30000, mode=1, callback=lambda t:p_time(rtc.datetime()))
tim2 = Timer(0)
# tim3 = Timer(2)
sw.irq(trigger=Pin.IRQ_FALLING, handler=cancel_de)

freq_r = 0 
while True:   
    if interruptf % 2:
        t = adc.read()
        pwm_r.deinit()
        led.off()
        sleep(1*t/511)
        led.on()
        sleep(1*t/511)
        freq_r = 1*t/511
    elif interruptf % 2 == 0 and interruptf > 0:
        pwm_g = PWM(Pin(12), freq=10, duty=(int(adc.read()/511*256)))
        led.off()
        sleep(freq_r)
        led.on()
        sleep(freq_r)
    else:
        None
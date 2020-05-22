from machine import Pin, Timer, I2C, PWM
from time import sleep

#Initialization
switch1 = Pin(12, Pin.IN, Pin.PULL_DOWN)
switch2 = Pin(27, Pin.IN, Pin.PULL_DOWN)
g_led = Pin(33, Pin.OUT)
r_led = Pin(15, Pin.OUT)
y_led = Pin(32, Pin.OUT)
led_board = Pin(13, Pin.OUT)
pwm = PWM(Pin(13), freq=10, duty=512)
pwm.deinit()
interrupt2 = 0
addr_list = []
temp_last = 0
pre_x = 0
pre_y = 0
pre_z = 0
vel_x = 0
vel_y = 0
vel_z = 0
pre_vel_x = 0
pre_vel_y = 0
pre_vel_z = 0
#Switch 1 interrupt
def call(pin):
    global interrupt2
    pwm.deinit()
    led_board = Pin(13, Pin.OUT)
    led_board.value(1)
    initialize()
    print("Waiting for calibrating")
    x,y,z = calibration()
    print("Calibration Done. The offset value is x:{},y:{},z:{}".format(x,y,z))
    interrupt2 = 0
def cancel_de(pin):
    tim.init(period=300, mode=Timer.ONE_SHOT, callback=call)

#Switch 2 interrupt
def call2(pin):
    global interrupt2
    interrupt2 = 1
def cancel_de2(pin):
    tim2.init(period=300, mode=Timer.ONE_SHOT, callback=call2)
    
tim = Timer(1)
tim2 = Timer(2)
switch1.irq(trigger=Pin.IRQ_FALLING, handler=cancel_de)
switch2.irq(trigger=Pin.IRQ_FALLING, handler=cancel_de2)
i2c = I2C(scl=Pin(22), sda=Pin(23),freq=400000)
acc_id = list(i2c.scan())[1]
temp_id = list(i2c.scan())[0]

def initialize():
    addr_list = list(i2c.scan())
    acc_addr = i2c.readfrom_mem(addr_list[1],0,1) 
    temp_addr = i2c.readfrom_mem(addr_list[0],0x0b,1)

    if acc_addr != b'\xe5':
        raise error('Wrong accelerometer device')
    if temp_addr != b'\xcb':
        raise error('Wrong temperature device')

    i2c.writeto_mem(acc_id,0x2d, b'\x08') #Mearsure
    i2c.writeto_mem(acc_id,0x2c, b'\x13') #800Hz-ODR
    i2c.writeto_mem(acc_id,0x31, b'\x08') #Full_Res & Range
    print("Accelerometer Sensor Initialized, Sensor id:{}".format(acc_addr))
    i2c.writeto_mem(temp_id,0x03, b'\x80') #16-bit-Res
    print("Temperature Sensor Initialized, Sensor id:{}".format(temp_addr))

def temp_trans(data,bit):
    if (data & (1 << (bit-1))):
        data = data - (1 << bit)
        return (data - 65536) / 128
    else:
        return data / 128
    return data

def acc_trans(data, bit):
    if (data & (1 << (bit-1))):
        data = data - (1 << bit)
    return data

def calibration():
    clear = bytearray([0, 0, 0])
    i2c.writeto_mem(acc_id,0x1E,clear)
    read = bytearray(6)
    x_offset = 0
    y_offset = 0
    z_offset = 0
    c = 0
    while c < 5000:   
        i2c.readfrom_mem_into(acc_id,0x32,read)
        value_x = (read[1] << 8 | read[0]) & 1023
        value_x = acc_trans(value_x, 10)
        value_y = (read[3] << 8 | read[2]) & 1023
        value_y = acc_trans(value_y, 10)
        value_z = (read[5] << 8 | read[4]) & 1023
        value_z = acc_trans(value_z,10)
        x_offset = x_offset + value_x
        y_offset = y_offset + value_y
        z_offset = z_offset + value_z
        c = c + 1
    x_offset = -int((x_offset / 5000) / 4)
    y_offset = -int((y_offset / 5000) / 4)
    z_offset = -int((z_offset / 5000) / 4)
    offset = bytearray([x_offset])
    i2c.writeto_mem(acc_id,0x1E,offset)
    offset = bytearray([y_offset])
    i2c.writeto_mem(acc_id,0x1F,offset)
    offset = bytearray([z_offset])
    i2c.writeto_mem(acc_id,0x20,offset)

    i2c.readfrom_mem_into(acc_id, 0x32,read)
    x = (read[1] << 8 | read[0]) & 1023
    x = acc_trans(x, 10)
    y = (read[3] << 8 | read[2]) & 1023
    y = acc_trans(y, 10)
    z = (read[5] << 8 | read[4]) & 1023
    z = acc_trans(z, 10) - offset[0]
    sleep(1)
    return x,y,z

while True:
    if interrupt2 > 0:
        led_board.value(0)
        pwm.init()
        offset = bytearray(1)
        i2c.readfrom_mem_into(acc_id,0x20,offset)
        
        read = bytearray(6)
        i2c.readfrom_mem_into(acc_id,0x32,read)
        value_x = (read[1] << 8 | read[0]) & 1023
        value_x = acc_trans(value_x, 10)
        value_y = (read[3] << 8 | read[2]) & 1023
        value_y = acc_trans(value_y, 10)
        value_z = (read[5] << 8 | read[4]) & 1023
        value_z = acc_trans(value_z,10) / acc_trans(value_z,10)

        vel_x = pre_vel_x + value_x * 0.3
        vel_y = pre_vel_y + value_y * 0.3
        vel_z = pre_vel_z + value_z * 0.3
        
        if abs(vel_x) > 10 or abs(vel_y) > 10 or abs(vel_z) > 10:
            r_led.value(1)
        else:
            r_led.value(0)
        print("The speeds are: {},{},{}".format(vel_x,vel_y,vel_z))
        
        angle_x = -value_x / 256 * 90
        angle_y = -value_y / 256 * 90
        angle_z = -value_z / 256 * 90
        if abs(angle_x) >= 30 or abs(angle_y) >= 30 or abs(angle_z) >= 30:
            y_led.value(1)
        else:
            y_led.value(0)
        print("The tilt angles are: {},{},{}".format(angle_x,angle_y,angle_z))
        if int(pre_x):
            if abs(pre_x - value_x) > 15 or abs(pre_y - value_y)> 15 or abs(pre_z - value_z) >15:
                g_led.value(0)
            else:
                g_led.value(1)
                pre_vel_x = 0
                vel_x = 0
                pre_vel_y = 0
                vel_y = 0
                pre_vel_z = 0
                vel_z = 0
        pre_x = value_x
        pre_y = value_y
        pre_z = value_z
        pre_vel_x = vel_x
        pre_vel_y = vel_y
        pre_vel_z = vel_z
        temp_data = bytearray(2)
        i2c.readfrom_mem_into(temp_id,0x00,temp_data)
        value = int.from_bytes(temp_data[0:2], "big")
        temp_data_dec = temp_trans(value,16)
        if (temp_last):
            freq = pwm.freq() + int((temp_last - temp_data_dec)) * 5
            pwm.freq(freq) 
        print("Current temperature is {}".format(temp_data_dec))
        temp_last = temp_data_dec
        sleep(0.3)

        


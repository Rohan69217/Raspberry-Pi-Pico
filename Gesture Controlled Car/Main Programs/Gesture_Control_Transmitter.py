import time
import utime
import struct
import machine
from machine import Pin, SPI, I2C
from nrf24l01 import NRF24L01
from imu import MPU6050
from time import sleep
import math
import array

i2c = I2C(1, sda=Pin(10), scl=Pin(11), freq=400000)
imu = MPU6050(i2c)

gyro_data = array.array('f', [0, 0])

spi = machine.SPI(0, sck=Pin(6), mosi=Pin(3), miso=Pin(4))

#nrf24l01 module connections
csn = machine.Pin(5, mode=Pin.OUT, value=1)
ce = machine.Pin(17, mode=Pin.OUT, value=0)
nrf = NRF24L01(spi, csn, ce, channel=0, payload_size=32)

nrf.open_tx_pipe(b'1Node')
nrf.open_rx_pipe(1, b'2Node')

nrf.stop_listening()

print("Transmitter Initialized")

while True:
    try:
        ax = round(imu.accel.x, 2)
        ay = round(imu.accel.y, 2)
        az = round(imu.accel.z, 2)
    
        angle_x = (math.asin((ax)/math.sqrt((ax ** 2)+(ay ** 2)+(az ** 2))) * 180)/3.14
        angle_y = (math.asin((ay)/math.sqrt((ax ** 2)+(ay ** 2)+(az ** 2))) * 180)/3.14

        gyro_data[0] = round(angle_x, 2)
        gyro_data[1] = round(angle_y, 2)
        
        data = struct.pack('ff', *gyro_data)
        nrf.send(data)
        print('Sent:', gyro_data)
        
        sleep(0.01)
            
    except OSError as e:
        print("Send failed:", e)
        time.sleep(0.1)
from machine import Pin, I2C
from time import sleep
import network
import socket

ssid = "your wifi name"
password = "your wifi password"

#local port and device id can be anything
#keep local port between 1024 and 9000
localPort = 8765
deviceID = "1"
dest_ip = "Ip address of device that data has to be sent to"

MPU6050_ADDR = 0x68
temp_register = 0x41
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
PWR_MGMT_1 = 0x6B

i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400000)

i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, b'\x00')

def read_raw_data(addr):
    try:
        high = i2c.readfrom_mem(MPU6050_ADDR, addr, 1)[0]
        low = i2c.readfrom_mem(MPU6050_ADDR, addr + 1, 1)[0]
        
        value = (high << 8) | low

        if value > 32767:
            value -= 65536

        return value
    except Exception as e:
        print("Error reading raw data:", e)
        return 0

def Get_Acc_Data():
    try:
        accel_x = read_raw_data(ACCEL_XOUT_H)
        accel_y = read_raw_data(ACCEL_YOUT_H)
        accel_z = read_raw_data(ACCEL_ZOUT_H)
        
        print(f"Raw Data - X: {accel_x}, Y: {accel_y}, Z: {accel_z}")  # Debug print
        
        accel_x = accel_x / 16384.0
        accel_y = accel_y / 16384.0
        accel_z = accel_z / 16384.0
        
        return accel_x, accel_y, accel_z
    except Exception as e:
        print("Error getting accelerometer data:", e)
        return 0, 0, 0

def connect_wifi():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                print('Connecting to network...')
                sleep(1)
        print('Network config:', wlan.ifconfig())
    except Exception:
        print("Error connecting to WiFi")

def send_udp(data):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(data.encode(), (dest_ip, localPort))
    except Exception:
        print("Error sending UDP data")
    finally:
        udp_socket.close()

connect_wifi()
while True:
    accel_x, accel_y, accel_z = Get_Acc_Data()
    accel_x *= 90
    accel_y *= 90
    accel_z *= 90
    data = "{:.2f},{:.2f},{:.2f}".format(-1*accel_x, -1*accel_y, -1*accel_z)
    send_udp(data)
    print("Sent Data  : ", data)
    sleep(0.1)

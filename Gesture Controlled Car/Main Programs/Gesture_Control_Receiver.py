import time
import utime
import struct
import machine
from machine import Pin, SPI, PWM
from nrf24l01 import NRF24L01

led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)

Front_Motor_1 = Pin(15, Pin.OUT)
Front_Motor_2 = Pin(14, Pin.OUT)
Back_Motor_1 = Pin(13, Pin.OUT)
Back_Motor_2 = Pin(12, Pin.OUT)
motor_b_pwm = PWM(Pin(11))
motor_b_pwm.freq(1000)
motor_a_pwm = PWM(Pin(10))
motor_a_pwm.freq(1000)


def Go_Forward(speed):
    motor_b_pwm.duty_u16(int(speed * 65535 / 100))
    Back_Motor_1.value(1)
    Back_Motor_2.value(0)
    print("Going Forward")
    
def Go_Backward(speed):
    motor_b_pwm.duty_u16(int(speed * 65535 / 100))
    Back_Motor_1.value(0)
    Back_Motor_2.value(1)
    print("Going Backward")
    
def Tilt_Right():
    motor_a_pwm.duty_u16(int(100 * 65535 / 100))
    Front_Motor_1.value(1)
    Front_Motor_2.value(0)
    print("Tilting Left")
    
def Tilt_Left():
    motor_a_pwm.duty_u16(int(100 * 65535 / 100))
    Front_Motor_1.value(0)
    Front_Motor_2.value(1)
    print("Tilting Right")
    
def Turn_Right_Forward(speed):
    motor_b_pwm.duty_u16(int((speed+50) * 65535 / 100))
    motor_a_pwm.duty_u16(int(100 * 65535 / 100))
    Front_Motor_1.value(1)
    Front_Motor_2.value(0)
    Back_Motor_1.value(1)
    Back_Motor_2.value(0)
    print("Turning Left")
    
def Turn_Left_Forward(speed):
    motor_a_pwm.duty_u16(int(100 * 65535 / 100))
    motor_b_pwm.duty_u16(int((speed+50) * 65535 / 100))
    Front_Motor_1.value(0)
    Front_Motor_2.value(1)
    Back_Motor_1.value(1)
    Back_Motor_2.value(0)
    print("Turning Right")
    
def Turn_Right_Backward(speed):
    motor_a_pwm.duty_u16(int(100 * 65535 / 100))
    motor_b_pwm.duty_u16(int((speed+50) * 65535 / 100))
    Front_Motor_1.value(1)
    Front_Motor_2.value(0)
    Back_Motor_1.value(0)
    Back_Motor_2.value(1)
    print("Turning Left(backward)")
    
def Turn_Left_Backward(speed):
    motor_a_pwm.duty_u16(int(100 * 65535 / 100))
    motor_b_pwm.duty_u16(int((speed+50) * 65535 / 100))
    Front_Motor_1.value(0)
    Front_Motor_2.value(1)
    Back_Motor_1.value(0)
    Back_Motor_2.value(1)
    print("Turning Right(backward)")
    
def Stop():
    Front_Motor_1.value(0)
    Front_Motor_2.value(0)


spi = machine.SPI(0, sck=Pin(6), mosi=Pin(3), miso=Pin(4))

csn = machine.Pin(5, mode=Pin.OUT, value=1)
ce = machine.Pin(17, mode=Pin.OUT, value=0)
nrf = NRF24L01(spi, csn, ce, channel=0, payload_size=32)

nrf.open_tx_pipe(b'2Node')
nrf.open_rx_pipe(1, b'1Node')

nrf.start_listening()

print("Receiver Initialized")

# Receive data
while True:
    try:
        if nrf.any():
            while nrf.any():
                data = nrf.recv()
                # Unpack
                received_data = struct.unpack('ff', data[:8])
                print('Received:', received_data)
                
                if received_data[0] > 20:
                    Go_Forward(received_data[0] * 100 / 80)
                    
                elif received_data[0] < -20:
                    Go_Backward(received_data[0] * 100 / 80)
                    
                elif received_data[1] > 20 and received_data[0] > 20:
                    Turn_Right_Forward(received_data[0] * 100 / 80)
                    
                elif received_data[1] < -20 and received_data[0] > 20:
                    Turn_Left_Forward(received_data[0] * 100 / 80)
                    
                elif received_data[1] > 20 and received_data[0] < -20:
                    Turn_Right_Forward(received_data[0] * 100 / 80)
                    
                elif received_data[1] < -20 and received_data[0] < -20:
                    Turn_Left_Forward(received_data[0] * 100 / 80)
                
                elif received_data[1] > 20:
                    Tilt_Left()
                    
                elif received_data[1] < -20:
                    Tilt_Right()
                    
                elif received_data[0] < 20 and received_data[0] > -20:
                    Back_Motor_1.value(0)
                    Back_Motor_2.value(0)
                
                if abs(received_data[1]) < 20 and abs(received_data[0]) < 90:
                    Stop()
                    
    except OSError as e:
        print("Receive failed:", e)
    time.sleep(0.01)
    
#     except KeyboardInterrupt:
#         Front_Motor_1.value(0)
#         Front_Motor_2.value(0)
#         Back_Motor_1.value(0)
#         Back_Motor_2.value(0)
        
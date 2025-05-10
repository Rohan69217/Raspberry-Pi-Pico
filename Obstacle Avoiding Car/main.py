from machine import Pin,PWM
import utime

class L298N_Driver:
    def __init__(self, a1, b1, a2, b2, ea, eb):
        self.motor1a = Pin(a1, Pin.OUT)
        self.motor1b = Pin(b1, Pin.OUT)
        self.motor2a = Pin(a2, Pin.OUT)
        self.motor2b = Pin(b2, Pin.OUT)
        self.enablea = PWM(Pin(ea))
        self.enableb = PWM(Pin(eb))
        self.enablea.freq(1000)
        self.enableb.freq(1000)
        
    def Go_Forward(self, speed):
        self.enableb.duty_u16(int(speed * 655.35))
        self.motor2a.high()
        self.motor2b.low()
    def Go_Backward(self, speed):
        self.enableb.duty_u16(int(speed * 655.35))
        self.motor2a.low()
        self.motor2b.high()
    def Turn_Left(self):
        self.enablea.duty_u16(65535)
        self.motor1a.high()
        self.motor1b.low()
    def Turn_Right(self):
        self.enablea.duty_u16(65535)
        self.motor1a.low()
        self.motor1b.high()
    def Stop(self):
        self.enableb.duty_u16(0)
        self.enablea.duty_u16(0)
        self.motor1a.low()
        self.motor1b.low()
        self.motor2a.low()
        self.motor2b.low()

        
class Ultrasonic:
    def __init__(self, t_pin, e_pin):
        self.Trigger = Pin(t_pin, Pin.OUT)
        self.Echo = Pin(e_pin, Pin.IN)
    
    def Get_Distance(self):
        self.Trigger.low()
        utime.sleep_us(2)
        
        self.Trigger.high()
        utime.sleep_us(5)
        
        self.Trigger.low()
        while self.Echo.value() == 0:
            off_time = utime.ticks_us()
            
        while self.Echo.value() == 1:
            on_time = utime.ticks_us()
            
        elapsed_time = utime.ticks_diff(ontime, offtime)
        return (elapsed_time * 0.0343)/2

class Servo:
    def __init__(self, Servo_Pin):
        self.pin = Pin(Servo_Pin, Pin.OUT)
        self.pin.freq(50)
    
    def set_servo_angle(self, angle):
        min_duty = 3277
        max_duty = 6553
    
        duty = int(min_duty + (max_duty - min_duty) * (angle / 180))
        self.pin.duty_u16(duty)

import time

import RPi.GPIO as GPIO
from simple_pid import PID

from movement import powertrain
from sensing import mpu6050

GPIO.setmode(GPIO.BCM)

# powertrain
POWERTRAIN_IN1_PIN = 19
POWERTRAIN_IN2_PIN = 13
POWERTRAIN_IN3_PIN = 6
POWERTRAIN_IN4_PIN = 5
POWERTRAIN_ENA_PIN = 26
POWERTRAIN_ENB_PIN = 11
MOTORSPEED_LEFT = 75
MOTORSPEED_RIGHT = 75


pt = powertrain.powertrain(
    POWERTRAIN_IN1_PIN,
    POWERTRAIN_IN2_PIN,
    POWERTRAIN_IN3_PIN,
    POWERTRAIN_IN4_PIN,
    POWERTRAIN_ENA_PIN,
    POWERTRAIN_ENB_PIN,
    MOTORSPEED_LEFT,
    MOTORSPEED_RIGHT)
    
mpu = mpu6050.mpu6050(0x68)

pt.change_speed_all(100)

###################### Testing

multiplier = 10

while True:
    angle = mpu.get_accel_data()['z']
    s = abs(angle)*multiplier
    s = 55 if s < 55 else s
    s = 100 if s > 100 else s
    pt.change_speed_all(s)

    if angle > 0:
        pt.move_front()
    else:
        pt.move_back()



###################### PID

setpoint = -0.38623979442138656
min_motor_speed = 55 # required for motors to start turning

Kp = 30
Ki = 0
Kd = 0

pid = PID(Kp, Ki, Kd, setpoint=setpoint, sample_time=0.007, output_limits=(-100, 100))
v = mpu.get_accel_data()['z']

old_time = time.time()

try:
   while(True):
        control = int(pid(v))
        if control < 0:
            pt.move_front()
        else:
            pt.move_back()
        control = abs(control)
        control = min_motor_speed if control < min_motor_speed else control
        pt.change_speed_all(control)
        current_time = time.time()
        print('V:', v, '| control:', control, '| Time elapsed (s):', current_time-old_time)
        old_time = current_time
        v = mpu.get_accel_data()['z']

except KeyboardInterrupt:
    print('Stopped!')

# mpu.get_accel_data()['z']
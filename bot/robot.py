import time

import RPi.GPIO as GPIO

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

while (True):
    print(mpu.get_all_data())
    time.sleep(0.1)
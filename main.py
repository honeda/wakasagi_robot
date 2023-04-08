from machine import Pin
import time

from wakasagi_robot.etc.servo import SG90
from wakasagi_robot.core.hit_detector import HitDetector

START_ANGLE = 87
END_ANGLE = 75
AWASE_ANGLE = 55

def awase(servo, hit_sensor):
    servo.write(AWASE_ANGLE)
    hit_sensor.remove_callback()


if __name__ == "__main__":

    servo = SG90(PWM(Pin(15, Pin.OUT)))
    hit_sensor = HitDetector(Pin(17, Pin.OUT, Pin.PULL_DOWN))

    servo.write2(AWASE_ANGLE, START_ANGLE, delay=10)
    for _ in range(3):
        servo.write2(START_ANGLE, END_ANGLE, delay=10)
        servo.write2(END_ANGLE, START_ANGLE, delay=10)
    time.sleep(1)
    hit_sensor.set_callback(lambda: awase(servo, hit_sensor))
    hit_sensor.wait()

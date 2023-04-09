from machine import Pin, PWM
import time

from wakasagi_robot.etc.servo import SG90, SG90_HV
from wakasagi_robot.core.hit_detector import HitDetector

START_ANGLE = 75
END_ANGLE = START_ANGLE - 15
AWASE_ANGLE = 1


def save_current_angle(angle):
    file = "data/last_angle.txt"
    with open(file, "w") as f:
        f.write(str(angle))
    print("Saved angle.", angle)

def load_last_angle():
    file = "data/last_angle.txt"
    try:
        with open(file) as f:
            return int(f.read())
    except OSError:
        return

def awase(servo, hit_sensor):
    servo.write(AWASE_ANGLE)
    save_current_angle(AWASE_ANGLE)
    hit_sensor.remove_callback()


if __name__ == "__main__":

    cur_angle = load_last_angle()
    if not cur_angle:
        cur_angle = START_ANGLE
    print(cur_angle)

    l293d_en1 = Pin(10, Pin.OUT)
    servo = SG90(PWM(Pin(14, Pin.OUT)))
    # dc_motor =
    hit_sensor = HitDetector(Pin(17, Pin.OUT, Pin.PULL_DOWN))

    servo.write2(cur_angle, START_ANGLE, delay=10)

    for _ in range(3):
        servo.write2(START_ANGLE, END_ANGLE, delay=10)
        servo.write2(END_ANGLE, START_ANGLE, delay=10)
    save_current_angle(START_ANGLE)
    time.sleep(1)
    hit_sensor.set_callback(lambda: awase(servo, hit_sensor))
    hit_sensor.wait()

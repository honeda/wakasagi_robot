from machine import Pin, PWM
import time

from wakasagi_robot.etc.utils import interval_mapping

class SG90:
    """
    SG90 is set to 0 degree at 0.5ms pulse width, and 180 degree at 2.4ms pulse width.
    And it accepts a pulse input every 20ms.
    Datasheet: https://akizukidenshi.com/download/ds/towerpro/SG90_a.pdf
    """
    min_angle = 0
    max_angle = 180
    min_palse_width = 0.5
    max_palse_width = 2.4
    interval = 20  # ms

    def __init__(self, pin_num:int):
        self.pin = PWM(Pin(pin_num))
        self.pin.freq(50)

    def write(self, angle:int):
        pulse_width = interval_mapping(
            angle,
            self.min_angle,
            self.max_angle,
            self.min_palse_width,
            self.max_palse_width
        )
        duty = int(interval_mapping(pulse_width, 0, self.interval, 0, 65535))
        self.pin.duty_u16(duty)

    def write2(self, start:int, end:int, step=1, delay=0):
        """
        Args:
            start (int): Start angle.
            end (int): End angle.
            step (int, optional): Step angle. Must be `step` > 0. Defaults to 1.
            delay (int, optional): Delay time [ms]. Defaults to 0.
        """
        if start < end:
            for angle in range(start, end + 1, step):
                self.write(angle)
                time.sleep_ms(self.interval + delay)
        else:
            for angle in range(start, end - 1, -step):
                self.write(angle)
                time.sleep_ms(self.interval + delay)

class SG90_HV:
    """360 degrees servo"""

    min_speed = 0
    max_speed = 180
    min_palse_width = 0.5
    max_palse_width = 2.4
    interval = 20  # ms

    def __init__(self, pin_num:int, offset=0):
        self.pin = PWM(Pin(pin_num))
        self.pin.freq(50)
        self.offset = offset

        self.stop_point = 90 + self.offset

    def write(self, speed:int):
        """
        Args:
            speed (int): 0~180
                0~89   -> clockwise
                91~180 -> counterclockwise
                90 -> stop
        """
        pulse_width = interval_mapping(
            speed + self.offset,
            self.min_speed,
            self.max_speed,
            self.min_palse_width,
            self.max_palse_width
        )
        duty = int(interval_mapping(pulse_width, 0, self.interval, 0, 65335))
        self.pin.duty_u16(duty)

    def stop(self):
        self.write(self.stop_point)

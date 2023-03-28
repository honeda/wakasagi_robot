from machine import Pin, PWM
import time

from utils import interval_mapping

class SG90:
    """
    SG90はパルス幅0.5msで０度, 2.5msで180度になる. そして20msごとにパルス入力を受け付ける
    """
    min_angle = 0
    max_angle = 180
    min_palse_width = 0.5
    max_palse_width = 2.5
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

    def go_angle(self, start:int, end:int, step=1, delay=0):
        """
        Args:
            start (int): Start angle.
            end (int): End angle
            step (int, optional): Step angle. Must be step > 0. Defaults to 1.
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

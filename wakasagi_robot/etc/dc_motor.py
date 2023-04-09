from machine import PWM
import time

class DCMotor:

    def __init__(self, cw_pin:PWM, ccw_pin=None):
        """
        Args:
            cw_pin(PWM): GPIO.
            ccw_pin(PWM, optional): Number of GPIO pin for GND side.
                Used to rotate in both directions. Defaults to None.
        """
        self.cw_pin = cw_pin
        self.ccw_pin = ccw_pin

    def rotate(self, duty_ratio, direction="cw"):
        """
        Args:
            duty_ratio (float): 0.0 <= duty_ratio <= 1.0.
            direction (str, optional): "cw" or "ccw". Defaults to "cw".
        """
        if direction == "cw":
            if self.ccw_pin:
                self.ccw_pin.duty_u16(0)
            self.cw_pin.duty_u16(int(65535 * duty_ratio))

        elif direction == "ccw" and self.ccw_pin:
            self.cw_pin.duty_u16(0)
            self.ccw_pin.duty_16(int(65535 * duty_ratio))

    def stop(self):
        self.cw_pin.duty_u16(0)
        if self.ccw_pin:
            self.ccw_pin.duty_u16(0)

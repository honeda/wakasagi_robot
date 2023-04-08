from machine import Pin
import time


class HitDetector:

    def __init__(self, pin:Pin):
        """
        Args:
            pin (Pin): Pull dowm pin. ex) `Pin(10, Pin.OUT, Pin.PULL_DOWN)`
        """
        self.pin = pin
        self.last_called_time = time.ticks_ms()
        self.callback = self._default_callback

    def wait(self):
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=lambda pin: self._detect(pin))

    def set_callback(self, func):
        """Set callback function to be called when hit is detected.

        Args:
            func (function): Callback function
        """
        self.callback = func

    def remove_callback(self):
        self.callback = self._default_callback
        self.wait()

    def _detect(self, pin):
        """Ignore inputs within 500ms."""
        if time.ticks_diff(time.ticks_ms(), self.last_called_time) < 500:
            return
        else:
            self.last_called_time = time.ticks_ms()
            self.callback()

    def _default_callback(self):
        return

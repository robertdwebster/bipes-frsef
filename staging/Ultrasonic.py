# Webster
# Arduino source: https://github.com/Seeed-Studio/Seeed_Arduino_UltrasonicRanger/blob/master/Ultrasonic.cpp

import time
from machine import Pin

class Ultrasonic:
    
    # Constructor - it has a pin number (an int)
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
    
    def duration(self, timeout):
        # Create a machine.Pin
        pin = Pin(self.pinNumber, Pin.OUT)
        pin.off()
        time.sleep_us(2)
        pin.on()
        time.sleep_us(5)
        pin.off()
        pin = Pin(self.pinNumber, Pin.IN)
        duration = Ultrasonic.pulseIn(pin, 1, timeout)
        return duration

    # Use ticks_diff(end, begin) where the parameters are microsecond tick variables returned by ticks_us()
    @staticmethod
    def pulseIn(pin, state, timeout):
        begin = time.ticks_us()

        # wait for any previous pulse to end
        while pin.value() == 1: 
            if (time.ticks_diff(time.ticks_us(), begin)) >= timeout:
                return 0

        # wait for the pulse to start
        while pin.value() == 0: 
            if (time.ticks_diff(time.ticks_us(), begin)) >= timeout:
                return 0
        pulseBegin = time.ticks_us()

        # wait for the pulse to stop
        while pin.value() == 1:
            if (time.ticks_diff(time.ticks_us(), begin)) >= timeout:
                return 0
        pulseEnd = time.ticks_us()

        return time.ticks_diff(pulseEnd, pulseBegin)

    def MeasureInCentimeters(self, timeout):
        RangeInCentimeters = self.duration(timeout) / 29 / 2
        return RangeInCentimeters
    
    def MeasureInMillimeters(self, timeout):
        RangeInMillimeters = self.duration(timeout) * (10 / 2) / 29
        return RangeInMillimeters

    def MeasureInInches(self,  timeout):
        RangeInInches = self.duration(timeout) / 74 / 2
        return RangeInInches


# Example code / "main" function below
myUltrasonic = Ultrasonic(16)
while True:
    MeasureInMillimeters = myUltrasonic.MeasureInMillimeters(1000000)
    print(str(MeasureInMillimeters) + " mm")
    time.sleep_ms(250)

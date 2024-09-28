from machine import Pin
from machine import PWM # don't forget this
from machine import ADC # don't forget this
import time

#frsef_grove_board_init:
def grove_connector_lookup_pin1(x):
		return {'UART0': 1,'UART1': 5,'D16': 16,'D18': 18,'D20': 20,'I2C0': 9,'I2C1': 7,'A0': 26,'A1': 27,'A2': 28,}[x]
def grove_connector_lookup_pin2(x):
		return {'UART0': 0,'UART1': 4,'D16': 17,'D18': 19,'D20': 21,'I2C0': 8,'I2C1': 6,'A0': 26,'A1': 26,'A2': 27,}[x]

# --- BUZZER ---
buzzer_dict = {}

def buzzer_get(connectorName):
    if connectorName not in buzzer_dict:
        pinNumber = grove_connector_lookup_pin1(connectorName)
        buzzer_dict[connectorName] = PWM(Pin(pinNumber))
        buzzer_dict[connectorName].freq(888)
    return buzzer_dict[connectorName]


# --- LED BUTTON ---
class LEDButton:

    def __init__(self, connectorName: str):
        self.LED = Pin(grove_connector_lookup_pin1(connectorName), Pin.OUT)
        self.Button = Pin(grove_connector_lookup_pin2(connectorName), Pin.IN)

    def LED_out(self, x):
        self.LED.value(x)

    def button_in(self):
        return not self.Button.value()

LED_button_dict = {}

def led_button_get(connectorName) -> LEDButton:
    if connectorName not in LED_button_dict:
        LED_button_dict[connectorName] = LEDButton(connectorName)
    return LED_button_dict[connectorName]


# --- Mini PIR Motion Sensor ---
motion_sensor_dict = {}

def motion_sensor_get(connectorName):
    if connectorName not in motion_sensor_dict:
        pinNumber = grove_connector_lookup_pin1(connectorName)
        motion_sensor_dict[connectorName] = Pin(pinNumber, Pin.IN)
    return motion_sensor_dict[connectorName]


# --- Analog Sensors: Loudness, Light, etc. ---
analog_in_dict = {}

def analog_sensor_get(connectorName):
    if connectorName not in analog_in_dict:
        pinNumber = grove_connector_lookup_pin1(connectorName)
        analog_in_dict[connectorName] = ADC(pinNumber)
    return analog_in_dict[connectorName]


# --- Ultrasonic Ranger ---
class Ultrasonic:
    
    # Constructor - it has a pin number (an int)
    def __init__(self, connectorName: str):
        self.pinNumber = grove_connector_lookup_pin1(connectorName)
        self.timeout = 100000
    
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

    def MeasureInCentimeters(self):
        RangeInCentimeters = self.duration(self.timeout) / 29 / 2
        return RangeInCentimeters
    
    def MeasureInMillimeters(self):
        RangeInMillimeters = self.duration(self.timeout) * (10 / 2) / 29
        return RangeInMillimeters

    def MeasureInInches(self):
        RangeInInches = self.duration(self.timeout) / 74 / 2
        return RangeInInches

ultrasonic_dict = {}

def ultrasonic_get(connectorName) -> Ultrasonic:
    if connectorName not in ultrasonic_dict:
        ultrasonic_dict[connectorName] = Ultrasonic(connectorName)
    return ultrasonic_dict[connectorName]


# --- Chained LED ---
class P9813:
    def __init__(self, num_leds, auto_write=True):
        self._num = num_leds
        self.auto_write = auto_write
        self.reset()

    def __setitem__(self, index, val):
        # (r, g, b) = val
        if isinstance(index, slice):
            start, stop, step = index.indices(self._num)
            length = stop - start
            if step != 0:
                length = (length + step - 1) // step
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match.")
            for val_i, idx_i in enumerate(range(start, stop, step)):
                self._set_led(idx_i, val[val_i])
        else:
            self._set_led(index, val)

        if self.auto_write:
            self.write()

    def __getitem__(self, index):
        # returns (r, g, b) if index is an int, eg. self[1]
        # or [(r, g, b), (r, g, b)] if index is a slice, eg. self[1:2]
        if isinstance(index, slice):
            out = []
            for idx_i in range(*index.indices(self._num)):
                out.append(self._get_led(idx_i))
            return out
        if index < 0:
            index += len(self)
        if index >= self._num or index < 0:
            raise IndexError
        return self._get_led(index)

    def __repr__(self):
        return "[" + ", ".join([str(x) for x in self]) + "]"

    def __len__(self):
        return self._num

    def _set_led(self, index, val):
        (r, g, b) = val
        # checksum bits (1, 1, blue[7], blue[6], green[7], green[6], red[7], red[6])
        self._buf[4 * index] = (
            0xC0 | (b & 0xC0) >> 2 | (g & 0xC0) >> 4 | (r & 0xC0) >> 6
        )
        # blue, green, red
        self._buf[4 * index + 1] = b
        self._buf[4 * index + 2] = g
        self._buf[4 * index + 3] = r

    def _get_led(self, index):
        # returns (r, g, b)
        return tuple(self._buf[index * 4 + i] for i in range(3, 0, -1))

    def fill(self, color):
        temp = self.auto_write
        self.auto_write = False
        for i in range(self._num):
            self[i] = color
        self.auto_write = temp
        if self.auto_write:
            self.write()

    def reset(self):
        self._buf = bytearray(self._num * 4)
        # checksums
        for i in range(0, self._num * 4, 4):
            self._buf[i] = 0xC0
        self.write()

    def write(self):
        raise NotImplementedError


class P9813_BITBANG(P9813):
    def __init__(self, pin_clk, pin_data, num_leds, auto_write=True):
        self._clk = pin_clk
        self._dat = pin_data
        self._clk.init(Pin.OUT)
        self._dat.init(Pin.OUT)
        super().__init__(num_leds, auto_write)

    def write(self):
        # Begin data frame 4 bytes
        self._frame()

        # Send 4 bytes for each LED (checksum, blue, green, red)
        for i in range(self._num):
            # Send checksum
            self._write_byte(self._buf[4 * i])
            # Send the 3 colours
            self._write_byte(self._buf[4 * i + 1])  # blue
            self._write_byte(self._buf[4 * i + 2])  # green
            self._write_byte(self._buf[4 * i + 3])  # red

        # End data frame 4 bytes
        self._frame()

    def _frame(self):
        # Send 32x zeros
        self._dat(0)
        for _ in range(32):
            self._clk_pulse()

    def _clk_pulse(self):
        self._clk(0)
        self._clk(1)

    def _write_byte(self, b):
        if b == 0:
            # Fast send 8x zeros
            self._dat(0)
            for _ in range(8):
                self._clk_pulse()
        else:
            # Send each bit, MSB first
            for i in range(8):
                if (b & 0x80) != 0:
                    self._dat(1)
                else:
                    self._dat(0)
                self._clk_pulse()

                # On to the next bit
                b <<= 1

chainable_LED_dict = {}

def chainable_LED_get(connectorName) -> P9813_BITBANG:
    if connectorName not in chainable_LED_dict:
        pin_clk = Pin(grove_connector_lookup_pin1(connectorName), Pin.OUT)
        pin_data = Pin(grove_connector_lookup_pin2(connectorName), Pin.OUT)
        chainable_LED_dict[connectorName] = P9813_BITBANG(pin_clk, pin_data, 1) # Todo: the number could be a parameter
    return chainable_LED_dict[connectorName]
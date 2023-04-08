from machine import ADC, Pin, Signal, Timer, I2C
import time
import ssd1306

pulse=ADC(26)


led = Pin(21, Pin.OUT)
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

MAX_HISTORY = 500

# Maintain a log of previous values to
# determine min, max and threshold.
history = []
beat = False
beats = 0

def calculate_bpm(t):
    oled.fill(0)
    oled.show()
    global beats
    print('BPM:', beats * 6)
    beats_oled = beats * 6
    beats = 0
    oled.text('BPM:', 0, 24)
    oled.text(str(beats_oled), 48, 24)
    oled.show()

timer = Timer(-1)
timer.init(period=10000, mode=Timer.PERIODIC, callback=calculate_bpm)

while True:
    v = pulse.read_u16()

    history.append(v)

    # Get the tail, up to MAX_HISTORY length
    history = history[-MAX_HISTORY:]

    min_value, max_value = min(history), max(history)

    threshold_on = (min_value + max_value * 3) // 4
    threshold_off = (min_value + max_value) // 2

    if not beat and v > threshold_on:
        beat = True
        beats += 1
        led.on()

    if beat and v < threshold_off:
        beat = False
        led.off()

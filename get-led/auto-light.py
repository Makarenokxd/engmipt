import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led, GPIO.OUT)

sensor = 6
GPIO.setup(sensor, GPIO.IN)

while True:
    GPIO.output(led, not GPIO.input(sensor))
    time.sleep(0.1)
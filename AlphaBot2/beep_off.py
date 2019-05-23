import RPi.GPIO as GPIO

BUZ = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZ, GPIO.OUT)
GPIO.output(BUZ, GPIO.LOW)
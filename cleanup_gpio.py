import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
GPIO.cleanup()
if len(sys.argv) == 2:
    pin = int(sys.argv[1])
    GPIO.setup(pin,GPIO.OUT)
    GPIO.cleanup()

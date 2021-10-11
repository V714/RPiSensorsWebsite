
import RPi.GPIO
import RPi.GPIO as GPIO

class RPiRGBDiode:

    def __init__(self, red=26,green=19,blue=13):
        self.red = red
        self.green = green
        self.blue = blue
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(red,GPIO.OUT)
        GPIO.setup(blue,GPIO.OUT)
        GPIO.setup(green,GPIO.OUT)
        print("INTING")

    def setColor(self,values='false,false,false'):
        print("SETCOLOR"+values)
        values = values.split(',')
        if values[0]=='true':
            GPIO.output(self.red,GPIO.LOW)
        else:
            GPIO.output(self.red,GPIO.HIGH)

        if values[1]=='true':
            GPIO.output(self.green,GPIO.LOW)
        else:
            GPIO.output(self.green,GPIO.HIGH)

        if values[2]=='true':
            GPIO.output(self.blue,GPIO.LOW)
        else:
            GPIO.output(self.blue,GPIO.HIGH)


import Adafruit_DHT

class DHT11:

    def __init__(self, Number_of_GPIO=21):
        self.sensor = Adafruit_DHT.DHT11
        self.pin = Number_of_GPIO

    def temperature(self):
        humidity, temperature = Adafruit_DHT.read(self.sensor, self.pin)
        return temperature
    
    def humidity(self):
        humidity, temperature = Adafruit_DHT.read(self.sensor, self.pin)
        return humidity



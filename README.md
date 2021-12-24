This script runs web server and allow you to control devices connected to Raspberry Pi through any device connected to the same local network.

Simply run by command
> python3 main.py

Web app opens on your local IP and port 5000, you can see the address on the terminal aswell.

To add RGB Diode ( __common cathode__ ) press **+** in yellow circle, select RGB Diode from list and type in numbers of GPIOs (__BCM numbering - not BOARD __) for specific colors.

Then simply go to **ip_of_rpi:5000/device/__number_of_your_device__**
If you don't know the number, you can go to **ip_of_rpi:5000/devices** to see all added devices.

You can also connect Temperature & Humidity sensor (**DHT 11** only for now) same way, and see the data from livestream (refreshes every few tens of seconds due to sensor limitations).

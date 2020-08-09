import time
import _thread
from lib.bme import BME
import struct
from lib.pir import PIR
from network import Sigfox
import socket

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink (Disabled downlink for now)
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# PIR (Output to pin 13 (G5))
pir = PIR('G5')
_thread.start_new_thread(pir.run_pir, ())

# BME680 (Output to Pin 9 and 10 (G16 and G17))
bme = BME(('P9', 'P10'))

while True:
    # Get the movement count since last time (Currently once / hour)
    count_last_hour = pir.get_count_last_h()

    # Get air condition values
    temp, humidity, pressure, air_quality = bme.get_values()

    # Print all
    print(temp, humidity, pressure, air_quality, count_last_hour)

    # Prepare the data by packing it before sending it to sigfox

    # Payload format is: >bBHHH where
    # b = Temperature (1 byte, 8 bits, signed) Range: -128 to 127
    # B = Humidity (1 byte, 8 bits, unsigned) Range: 0 to 255
    # H = Pressure (2 bytes, 16 bits, unsigned) Range: 0 to 65,535
    # B = Air Quality (2 byte, 16 bits, unsigned) Range: 0 to 65,535
    # I = Movement last hour (2 bytes, 16 bits, unsigned) Range: 0 to 65,535
    package = struct.pack('>bBHHH', int(temp), int(humidity), int(pressure), int(air_quality), int(count_last_hour))

    # Send the data to sigfox backend
    s.send(package)

    # Sleep for 60 minutes
    time.sleep(3600)

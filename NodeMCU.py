import RPi.GPIO
import sys
import time
import busio
import board

i2c = i2c = busio.I2C(board.SCL, board.SDA)
print("I2C Devices Found:", [hex(i) for i in i2c.scan()])
NodeMCU = 0x12

if NodeMCU not in i2c.scan():
    print("Not Found")
    sys.exit()

def get_data():
    while True:
        i2c.writeto(NodeMCU, bytes([0x00]), stop=False)
        result = bytearray(1)
        i2c.readfrom_into(NodeMCU, result)
        print("value: ", int.from_bytes(result, "big"))
        time.sleep(1)

if __name__ == "__main__":
    get_data()
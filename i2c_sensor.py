import sys
import RPi.GPIO as GPIO
import board
import busio

i2c = busio.I2C(board.SCL,board.SDA)
print("I2C Devices Found:", [hex(i) for i in i2c.scan()])
bmp = 0x76

if not bmp in i2c.scan():
	print("Not Found")
	sys.exit()

def get_id():
	i2c.writeto(bmp,bytes([0xD0]), stop=False)
	result = bytearray(1)
	i2c.readfrom_into(bmp,result)
	print("ID: ", int.from_bytes(result,"big"))
	i2c.writeto(bmp,bytes([0xF4]),stop = False)
	i2c.writeto(0xF4,bytes([0b11]),stop=True)
	i2c.writeto(bmp,bytes([0xF4]), stop=False)
	result = bytearray(1)
	i2c.readfrom_into(bmp,result)
	print("F4 config:",int.from_bytes(result,"big"))

if __name__ == "__main__":
	get_id()

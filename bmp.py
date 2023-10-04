import sys
import RPi.GPIO as GPIO
import board
import busio
import time
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C Devices Found:", [hex(i) for i in i2c.scan()])
bmp = 0x76

if bmp not in i2c.scan():
    print("Not Found")
    sys.exit()

def get_id():
    i2c.writeto(bmp, bytes([0xD0]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(bmp, result)
    print("ID: ", int.from_bytes(result, "big"))

    i2c.writeto(bmp, bytes([0xF5, 0b01010000]), stop=False)
    i2c.writeto(bmp, bytes([0xF4, 0b01010111]), stop=False)

    i2c.writeto(bmp, bytes([0xF4]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(bmp, result)
    print("F4 config:", int.from_bytes(result, "big"))

    i2c.writeto(bmp, bytes([0xF5]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(bmp, result)
    print("F5 config: ", int.from_bytes(result, "big"))

def calibrate():
    calibration_data = bytearray(24)
    for i in range(24):
        register_address = 0x88 + i
        i2c.writeto(bmp, bytes([register_address]), stop=False)
        i2c.readfrom_into(bmp, calibration_data[i:i+1])
    print(calibration_data,end="\n\n\n")
    return calibration_data


def get_reading():
    i2c.writeto(bmp,bytes([0xFA]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(bmp, result)
    print("msb: ", int.from_bytes(result,"big"),end="\t")
    temp = 0
    temp = (temp * 16) +int.from_bytes(result,"big")

    i2c.writeto(bmp,bytes([0xFB]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(bmp, result)
    print("lsb: ", int.from_bytes(result,"big"),end="\t")
    temp = (temp * 256) +int.from_bytes(result,"big")

    i2c.writeto(bmp,bytes([0xFC]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(bmp, result)
    result[0] = result[0]>>7
    print("xlsb: ", int.from_bytes(result,"big"),end="\t")

    temp = (temp * 2) +int.from_bytes(result,"big")
    temp = temp/100
    print("Temp: ", temp,end="\n\n") 

def dummy():
    calibration_data = calibrate()

    i2c.writeto(bmp,bytes([0xFA]), stop=False)
    raw_temp_msb = bytearray(1)
    i2c.readfrom_into(bmp, raw_temp_msb)

    i2c.writeto(bmp,bytes([0xFB]), stop=False)
    raw_temp_lsb = bytearray(1)
    i2c.readfrom_into(bmp, raw_temp_lsb)

    i2c.writeto(bmp,bytes([0xFC]), stop=False)
    raw_temp_xlsb = bytearray(1)
    i2c.readfrom_into(bmp, raw_temp_xlsb)

    # Combine the raw data into a 20-bit value
    raw_temperature = ((raw_temp_msb[0] << 16) | (raw_temp_lsb[0] << 8) | raw_temp_xlsb[0]) >> 4

    print(raw_temperature, end='\t')
    # Calculate the temperature using the calibration data
    dig_T1 = (calibration_data[1] << 8) | calibration_data[0]
    dig_T2 = (calibration_data[3] << 8) | calibration_data[2]
    dig_T3 = (calibration_data[5] << 8) | calibration_data[4]

    var1 = (raw_temperature / 16384.0 - dig_T1 / 1024.0) * dig_T2
    var2 = ((raw_temperature / 131072.0 - dig_T1 / 8192.0) ** 2) * dig_T3
    t_fine = var1 + var2

    temperature = (t_fine / 5120.0)  # Temperature in degrees Celsius

    print("Temp: ",temperature)
if __name__ == "__main__":
    get_id()
    while(True):
        dummy()
        time.sleep(1)

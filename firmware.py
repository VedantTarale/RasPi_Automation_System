import sys
import RPi.GPIO as GPIO
import board
import busio
import time
i2c = busio.I2C(board.SCL, board.SDA)
bmp = 0x76
NodeMCU = 0x12

pump = 16

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pump, GPIO.OUT)

def initialize():
    print("I2C Devices Found:", [hex(i) for i in i2c.scan()])
    if bmp not in i2c.scan():
        print("BMP280 Sensor Not Found")
        sys.exit()
    if NodeMCU not in i2c.scan():
        print("NodeMCU Not Found")
        sys.exit()
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

def get_bmp_reading():
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


    # Calculate the temperature using the calibration data
    dig_T1 = 27504
    dig_T2 = 26435
    dig_T3 = -1000

    var1 = (raw_temperature / 16384.0 - dig_T1 / 1024.0) * dig_T2
    var2 = ((raw_temperature / 131072.0 - dig_T1 / 8192.0) ** 2) * dig_T3
    t_fine = var1 + var2

    temperature = (t_fine / 5120.0)  # Temperature in degrees Celsius

    print("Temp: " + str(round(temperature,2)) + " ºC",end="\t")


    i2c.writeto(bmp,bytes([0xF7]), stop=False)
    raw_pressure_msb = bytearray(1)
    i2c.readfrom_into(bmp, raw_pressure_msb)

    i2c.writeto(bmp,bytes([0xF8]), stop=False)
    raw_pressure_lsb = bytearray(1)
    i2c.readfrom_into(bmp, raw_pressure_lsb)

    i2c.writeto(bmp,bytes([0xF9]), stop=False)
    raw_pressure_xlsb = bytearray(1)
    i2c.readfrom_into(bmp, raw_pressure_xlsb)

    # Combine the raw data into a 20-bit value
    raw_pressure = ((raw_pressure_msb[0] << 16) | (raw_pressure_lsb[0] << 8) | raw_pressure_xlsb[0]) >> 4

    dig_P1 = 36477
    dig_P2 = -10685
    dig_P3 = 3024
    dig_P4 = 2855
    dig_P5 = 140
    dig_P6 = -7
    dig_P7 = 15500
    dig_P8 = -14600
    dig_P9 = 6000

    var1 = (t_fine / 2.0) - 64000.0
    var2 = var1 * var1 * (dig_P6 / 32768.0)
    var2 = var2 + (var1 * dig_P5 * 2.0)
    var2 = (var2 / 4.0) + (dig_P4 * 65536.0)
    var1 = ((dig_P3 * var1 * var1) / 524288.0) + (dig_P2 * var1)
    var1 = ((1.0 + (var1 / 32768.0)) * dig_P1)

    if var1 == 0:
        pressure = 0  # Avoid division by zero
    else:
        pressure = 1048576.0 - raw_pressure
        pressure = (pressure - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (dig_P9 * pressure * pressure) / 2147483648.0
        var2 = pressure * (dig_P8 / 32768.0)
        pressure = pressure + ((var1 + var2 + dig_P7) / 16.0)
    print("Pressure: " + str(round(pressure,2)) + " hPa")

def get_NodeMCU_Reading():
    i2c.writeto(NodeMCU, bytes([0x00]), stop=False)
    result = bytearray(1)
    i2c.readfrom_into(NodeMCU, result)

    global water_reading
    water_reading = int.from_bytes(result, "big")

    print("value: ", int.from_bytes(result, "big"))
    time.sleep(1)

def pump_water():
    global water_reading
    final_val = 160 #to be modified later
    margin = 5 #to be modified later
    GPIO.output(pump,0)
    get_NodeMCU_Reading()
    try:
        while (final_val - water_reading) > margin:
            GPIO.output(pump,1)
            time.sleep(1)
            get_NodeMCU_Reading()
        print("done")
        GPIO.output(pump,0)
    except KeyboardInterrupt:
        GPIO.cleanup()

def get_reading():
    #calibration_data = calibrate()
    get_bmp_reading()
    get_NodeMCU_Reading()
    

if __name__ == "__main__":
    initialize()
    while True:
        get_reading()
        time.sleep(0.1)
##	calibrate()

import serial
import struct
import time

def send_command(command):
    ser.write(command)
    response = ser.read(ser.in_waiting)
    print(response)
    return response

def calculate_weight(data):
    weight = struct.unpack('>H', data[4:6])[0] * 65535 + struct.unpack('>H', data[6:8])[0]
    return weight

def calibrate_sensor():
    # 进入校准模式
    send_command(b'\x03\x06\x00\x0D\x00\x02\x98\x2A')
    send_command(b'\x03\x06\x00\x0D\x00\x02\x98\x2A')

    # 去皮清零
    send_command(b'\x03\x10\x00\x15\x00\x03\x06\x00\x01\x00\x00\x00\x00\xCD\x87')
    # send_command(b'\x03\x10\x00\x15\x00\x03\x90\x2E')

    # 校准
    # send_command(b'\x03\x06\x00\x0D\x00\x02\x98\x2A')
    # send_command(b'\x03\x06\x00\x0D\x00\x02\x98\x2A')
    send_command(b'\x03\x10\x00\x15\x00\x03\x06\x00\x02\x00\x00\x04\x4C\x8A\xB2')
    # send_command(b'\x03\x10\x00\x15\x00\x03\x90\x2E')

    # 校准保存
    send_command(b'\x03\x10\x00\x15\x00\x03\x06\x00\x03\x00\x00\x04\x4C\xB7\x72')
    # send_command(b'\x03\x10\x00\x15\x00\x03\x90\x2E')

    # 进入正常模式
    # send_command(b'\x03\x06\x00\x0D\x00\x00\x19\xEB')
    # send_command(b'\x03\x06\x00\x0D\x00\x00\x19\xEB')

def read_weight():
    while True:
        # 读取称重数据
        data = send_command(b'\x04\x03\x1A\x00\x00\x0D\x26\x00\x08\x05\x55\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x83\x10')
        weight = calculate_weight(data)
        print(f"Weight: {weight} g")
        time.sleep(1)

# 设置串口参数（根据实际情况修改）
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# 校准传感器
calibrate_sensor()

# 持续读取重量
# read_weight()

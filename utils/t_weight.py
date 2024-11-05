import serial
import struct
import time

def calculate_weight(data_bytes):
    # 解析重量数据
    # 假设数据为 response[3:7]，即4个字节表示重量数值
    weight_raw = struct.unpack('>HH', data_bytes)  # 大端模式两个无符号短整数
    weight = weight_raw[0] * 65535 + weight_raw[1]
    return weight

def read_sensor_data(port='/dev/ttyUSB0', baudrate=9600, timeout=1):
    try:
        # 打开串口
        ser = serial.Serial(port, baudrate, timeout=timeout)

        while True:  # 持续监控
            # 发送读状态命令
            # command = bytes([0x03, 0x03, 0x00, 0x00, 0x00, 0x0D, 0x85, 0xED])
            command = input("请输入以逗号分隔的16进制字节（例如：0x03, 0x06, 0x00, 0x0E, 0x00, 0x01, 0x28, 0x2B）：")
            # 将输入字符串分割并转换为整数，然后转为字节
            byte_list = [int(x.strip(), 16) for x in command.split(' ')]
            # ser.write(command)
            ser.write(byte_list)

            # time.sleep(0.1)  # 等待设备响应

            # 读取传感器返回数据
            response = ser.read(32)  # 假定响应的长度
            print(response)
            # 检查响应并解析数据
            if len(response) >= 29:  # 响应至少要有29字节
                # 提取重量数据
                weight_bytes = response[3:7]
                print(weight_bytes)
                weight = calculate_weight(weight_bytes)
                print(f"重量: {weight} g")

                # 检查满溢状态
                overflow_status = response[7:9]
                overflow_val = struct.unpack('>H', overflow_status)[0]
                is_full = overflow_val in (0x004A, 0x0048, 0x0002)
                print(f"满溢状态: {'满桶' if is_full else '正常'}")

            else:
                print("接收到的数据不足")

            # time.sleep(1)  # 等待1秒再进行下一次读取

    except serial.SerialException as e:
        print(f"串口错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if ser.is_open:
            ser.close()

if __name__ == "__main__":
    read_sensor_data()

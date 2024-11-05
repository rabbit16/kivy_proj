import serial
import time


def hex_string_to_bytes(hex_str):
    """将十六进制字符串转换为字节。"""
    return bytes.fromhex(hex_str)


def send_command(serial_port, cmd):
    """向串口发送命令。"""
    serial_port.write(hex_string_to_bytes(cmd))
    time.sleep(0.1)


def read_response(serial_port):
    """从串口读取响应。"""
    time.sleep(0.1)
    if serial_port.in_waiting > 0:
        response = serial_port.read_all()
        return response.hex()
    return None


def parse_weight_data(hex_data):
    """解析称重数据。"""
    if len(hex_data) >= 10:
        weight_hex = hex_data[6:14]  # 假设重量信息在特定位置
        weight1 = int(weight_hex[0:4], 16)  # 高位部分
        weight2 = int(weight_hex[4:8], 16)  # 低位部分
        weight = weight1 * 65536 + weight2
        return weight
    return None


def main():
    # 配置串口参数
    port = '/dev/ttyUSB0'  # 对于Windows，可能是 'COM3'，'COM4' 等
    baudrate = 9600

    # 读取称重指令
    read_command = '03030000000D85ED'

    # 打开串口
    with serial.Serial(port, baudrate, timeout=1) as ser:
        try:
            while True:
                # 发送读取称重的命令
                send_command(ser, read_command)

                # 读取并解析响应数据
                response = read_response(ser)
                if response:
                    print(f"响应数据: {response}")
                    weight = parse_weight_data(response)
                    if weight is not None:
                        print(f"当前重量: {weight} g")

                # 每隔一段时间读取一次数据
                # time.sleep(2)

        except KeyboardInterrupt:
            print("\n停止读取数据。")


if __name__ == '__main__':
    main()

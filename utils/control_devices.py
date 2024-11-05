import serial
import time


def read_pushrod_state(port='/dev/ttyUSB0', baudrate=9600):
    try:
        # 创建串口对象
        ser = serial.Serial(port, baudrate, timeout=1)

        # 等待串口准备好
        time.sleep(2)
        # ser.open()

        # 发送读取推杆状态的命令
        # command = bytes([0x03, 0x03, 0x00, 0x05, 0x00, 0x01, 0x95, 0xE9])
        while True:
            user_input = input("请输入以逗号分隔的16进制字节（例如：0x03, 0x06, 0x00, 0x0E, 0x00, 0x01, 0x28, 0x2B）：")
            # 将输入字符串分割并转换为整数，然后转为字节
            byte_list = [int(x.strip(), 16) for x in user_input.split(',')]
            # open_command = bytes([0x03, 0x06, 0x00, 0x0E, 0x00, 0x01, 0x28, 0x2B])  # 开门 0x03,0x06,0x00,0x0E,0x00,0x01,0x28,0x2B
            # close_command = bytes([0x03, 0x06, 0x00, 0x0E, 0x00, 0x01, 0x28, 0x2B])  # 关门 0x03,0x06,0x00,0x0E,0x00,0xFF,0xA9,0xCD
            # 读取状态指令 0x03,0x03,0x00,0x00,0x00,0x0D,0x85,0xED
            # 读取配置指令 0x03,0x03,0x00,0x1A,0x00,0x0A,0xE5,0xE8
            # 读取称重 0x03,0x03,0x00,0x00,0x00,0x0D,0x85,0xED
            ser.write(byte_list)

            # 从串口读取返回的数据 0x03,0x03,0x00,0x05,0x00,0x01,0x95,0xE9
            response = ser.read(64)  # 根据返回数据长度进行读取
            print(response)
            """
            b'\x03\x03\x02\x00\x00\xc1\x84' 看着像是从推杆回来后的状态
            b'\x03\x03\x02\x00\x01\x00D' 看着像是
             1. 68 推出
             2. 133 缩回
             3. 132 停止
             4. 69 保持
            """
            while True:
                ser.write([0x03, 0x03, 0x00, 0x05, 0x00, 0x01, 0x95, 0xE9])
                response = ser.read(64)  # 根据返回数据长度进行读取
                print(response[-1])
                print(response)
                see = input("是否继续：1 or 0")
                if see=="0":
                    break

        # 在这里进行解析返回的状态
        if response:
            state = response[3]  # 第4个字节是状态字节  这个是按字节读取，所以read也是读取字节
            if state == 0:
                print("状态: 停止")
            elif state == 1:
                print("状态: 推出")
            elif state == 2:
                print("状态: 保持")
            elif state == 3:
                print("状态: 缩回")
            else:
                print("状态未知")
        else:
            print("没有接收到回复")

    except serial.SerialException as e:
        print(f"串口错误: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()  # 关闭串口


if __name__ == "__main__":
    read_pushrod_state()

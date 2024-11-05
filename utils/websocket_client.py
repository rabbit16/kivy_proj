# client.py
import asyncio
import websockets
import cv2

async def send_video():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)  # 打开摄像头或提供视频文件路径

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # 编码图像为JPEG格式
            _, buffer = cv2.imencode('.jpg', frame)
            img_as_text = buffer.tobytes()

            # 发送图像数据
            await websocket.send(img_as_text)

            # 增加适当的延迟可以避免摄像头过载
            await asyncio.sleep(0.01)

        cap.release()

asyncio.get_event_loop().run_until_complete(send_video())

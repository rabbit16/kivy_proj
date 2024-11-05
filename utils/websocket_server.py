# server.py
import asyncio
import websockets
import cv2
import numpy as np


async def receive_image(websocket, path):
    while True:
        try:
            # 接收图像数据
            data = await websocket.recv()
            nparr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 用cv2展示图像
            cv2.imshow("Received Video", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    cv2.destroyAllWindows()


start_server = websockets.serve(receive_image, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

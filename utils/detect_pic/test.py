import torch
import cv2
import numpy as np

# 加载 YOLOv8 模型
model = torch.hub.load('ultralytics/yolov8', 'yolov8', pretrained=True)  # 加载预训练模型
# model = torch.load('path/to/your/yolov8.pt')  # 如果你有自己的模型文件，使用此行替代

# 设置输入图像
image = cv2.imread('input.jpg')  # 替换为你的输入图像路径
# 预处理
image_resized = cv2.resize(image, (640, 640))  # YOLOv8 默认输入大小为640x640
image_resized = image_resized[:, :, ::-1]  # BGR to RGB
image_resized = torch.from_numpy(image_resized).float()  # 转换为Tensor
image_resized /= 255.0  # 归一化
image_resized = image_resized.permute(2, 0, 1).unsqueeze(0)  # Change shape to [1,3,H,W]

# 推理
with torch.no_grad():  # 关闭梯度计算
    detections = model(image_resized)

# 处理输出
results = detections.xyxy[0]  # 获取检测结果 [xmin, ymin, xmax, ymax, confidence, class]

# 绘制检测框
for *box, conf, cls in results.tolist():
    x1, y1, x2, y2 = map(int, box)  # 转换为整数
    label = f'Class: {int(cls)}, Conf: {conf:.2f}'
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# 显示结果
cv2.imshow("Detections", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

import matplotlib.pyplot as plt

# 数据
labels = ['类别 A', '类别 B', '类别 C', '类别 D']
sizes = [15, 30, 45, 10]  # 各类别的大小
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']  # 各类别的颜色

# 绘制饼图
plt.figure(figsize=(8, 6))  # 设置图形大小
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

# 添加图例（在右侧）
plt.legend(title="类别和计数", loc="center left", bbox_to_anchor=(1, 0.5), labels=[f'{label} ({size})' for label, size in zip(labels, sizes)])

# 确保图形是圆形的，比例合适
plt.axis('equal')

# 显示图形
plt.tight_layout()  # 调整子图参数以适应图例
plt.show()

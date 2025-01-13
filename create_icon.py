from PIL import Image, ImageDraw, ImageFont
import os

# 創建一個 256x256 的圖像
size = 256
image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# 繪製圓形背景
circle_color = (255, 0, 0)  # 紅色
circle_radius = size // 2
circle_center = (size // 2, size // 2)
draw.ellipse([
    circle_center[0] - circle_radius,
    circle_center[1] - circle_radius,
    circle_center[0] + circle_radius,
    circle_center[1] + circle_radius
], fill=circle_color)

# 繪製播放按鈕
play_color = (255, 255, 255)  # 白色
triangle_size = size // 3
center_x = size // 2
center_y = size // 2
play_points = [
    (center_x - triangle_size//2, center_y - triangle_size//2),
    (center_x - triangle_size//2, center_y + triangle_size//2),
    (center_x + triangle_size//2, center_y),
]
draw.polygon(play_points, fill=play_color)

# 保存為 ICO 文件
image.save('icon.ico', format='ICO', sizes=[(256, 256)])

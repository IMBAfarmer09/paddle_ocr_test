import easyocr
from PIL import Image, ImageDraw

# 初始化阅读器，指定需要识别的语言
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

# 读取图像并进行文字识别
image_path = 'map.png'  # 替换为您的图像路径
results = reader.readtext(image_path)

# 打印识别结果
for idx, (bbox, text, prob) in enumerate(results):
    print(f'[{idx}] Text: {text}, Probability: {prob:.4f}, BBox: {bbox}')

# 使用 PIL 加载图像
image = Image.open(image_path)

# 创建绘图上下文
draw = ImageDraw.Draw(image)

# 开关：是否显示编号
show_numbers = True

# 绘制识别到的文本区域
for idx, (bbox, _, _) in enumerate(results):
    # 将浮点数坐标转换为整数
    polygon = [tuple(map(int, point)) for point in bbox]
    # 绘制多边形框
    draw.polygon(polygon, outline="red", width=3)

    # 在图像上显示编号（根据开关决定）
    if show_numbers:
        top_left = tuple(map(int, bbox[0]))  # 使用第一个点作为编号起始点
        draw.text((top_left[0], top_left[1] - 10), str(idx), fill="blue")

# 保存结果
output_path = 'easyocr_result.png'
image.save(output_path)
print(f'Result saved to {output_path}')

from PIL import Image, ImageDraw, ImageFont
import random
import json
import string

# 在 Windows 环境下使用默认字体
font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Arial 字体路径
font_size = 40
font = ImageFont.truetype(font_path, font_size)

# 随机生成文本
def generate_random_text(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 创建图像
def create_image_with_text(text, spacing=10):
    width = len(text) * font_size + spacing * (len(text) - 1)  # 增加间距后的宽度
    height = font_size + 20  # 留出一些空间给文本
    image = Image.new("RGB", (width, height), (255, 255, 255))  # 白色背景
    draw = ImageDraw.Draw(image)

    x_offset = 10  # 初始偏移量
    for char in text:
        # 获取字符的 bounding box
        bbox = draw.textbbox((x_offset, 10), char, font=font)
        # 绘制字符
        draw.text((x_offset, 10), char, font=font, fill=(0, 0, 0))  # 黑色文字
        # 更新偏移量：字符宽度加上额外的间距
        x_offset += bbox[2] - bbox[0] + spacing  # 每个字符宽度加上spacing

    return image

# 计算字符的 bounding box
def get_character_bboxes(text, spacing=10):
    bboxes = []
    x_offset = 10  # 偏移量，用于每个字符的起始位置

    # 创建一个空白图像并获取 draw 对象来计算字符尺寸
    dummy_image = Image.new("RGB", (1000, 100), (255, 255, 255))  # 预创建一个大图像
    draw = ImageDraw.Draw(dummy_image)

    for char in text:
        # 使用 textbbox 获取字符的边界框
        bbox = draw.textbbox((x_offset, 10), char, font=font)
        bboxes.append(bbox)
        x_offset += bbox[2] - bbox[0] + spacing  # 更新偏移量，加上额外的间距

    return bboxes


# 随机生成数据
def generate_data(num_images=10, spacing=10):
    data = []

    for i in range(num_images):
        text = generate_random_text(random.randint(3, 7))  # 随机生成3-7个字符的文本
        image = create_image_with_text(text, spacing=spacing)
        bboxes = get_character_bboxes(text, spacing=spacing)

        # 绘制bounding box
        draw = ImageDraw.Draw(image)
        for bbox in bboxes:
            draw.rectangle([bbox[0], bbox[1], bbox[2], bbox[3]], outline="red", width=2)

        # 保存图像
        image_filename = f"image_{i + 1}.png"
        image.save(image_filename)

        # 保存标注
        annotations = []
        for j, (char, bbox) in enumerate(zip(text, bboxes)):
            annotations.append({
                "character": char,
                "bbox": bbox,
                "category_id": j  # 每个字符类别可以根据索引生成
            })

        data.append({
            "image": image_filename,
            "annotations": annotations
        })

    # 保存JSON格式的标注文件
    with open("annotations.json", "w") as f:
        json.dump(data, f, indent=4)


# 生成 10 张带有字符 bounding box 标注的图像和真值标签
generate_data(num_images=10, spacing=5)  # 设置字符间距为 20 像素

print("生成的数据和标注已保存！")

from PIL import Image, ImageDraw, ImageFont
import random
import string
import json

# 设置字体和大小
font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Arial 字体路径
font_size = 40
font = ImageFont.truetype(font_path, font_size)

# 设置更小的字体用于上下标
subsup_font_size = int(font_size * 0.3)  # 上下标字体为普通字体的 30%
subsup_font = ImageFont.truetype(font_path, subsup_font_size)

# 打印字体大小以确认
print(f"Normal font size: {font_size}, Subscript/Superscript font size: {subsup_font_size}")

# 改进后的 generate_random_text，增加生成上标和下标字符的概率，并确保合理位置
def generate_random_text(length=5):
    characters = string.ascii_letters + string.digits  # 字母和数字
    text = ""

    # 随机生成字符
    for i in range(length):
        # 确保上下标不出现在第一个或最后一个字符
        if i > 0 and i < length - 1:  # 不在第一个和最后一个字符插入
            if random.random() < 0.1:  # 10% 概率插入上标字符
                text += "^"  # 上标符号
                text += random.choice(string.digits)  # 随机选择一个数字作为上标
            elif random.random() < 0.1:  # 10% 概率插入下标字符
                text += "_"  # 下标符号
                text += random.choice(string.digits)  # 随机选择一个数字作为下标
            else:
                text += random.choice(characters)  # 普通字符
        else:
            text += random.choice(characters)  # 普通字符

    return text


# 根据输入生成两个列表：字符列表和字符类型标识列表
def process_text(text):
    char_list = []
    char_type_list = []  # 'normal', 'superscript', 'subscript'

    i = 0
    while i < len(text):
        if text[i] == '^':  # 上标
            char_type_list.append('superscript')
            char_list.append(text[i + 1])  # 下一个字符为上标
            i += 2
        elif text[i] == '_':  # 下标
            char_type_list.append('subscript')
            char_list.append(text[i + 1])  # 下一个字符为下标
            i += 2
        else:
            char_type_list.append('normal')
            char_list.append(text[i])  # 普通字符
            i += 1
    return char_list, char_type_list


# 根据生成的 char_list 和 char_type_list 创建图像
def create_image_with_text(text, spacing=5):
    char_list, char_type_list = process_text(text)
    width = len(char_list) * font_size + spacing * (len(char_list) - 1)  # 增加间距后的宽度
    height = font_size + 20  # 留出一些空间给文本
    image = Image.new("RGB", (width, height), (255, 255, 255))  # 白色背景
    draw = ImageDraw.Draw(image)

    x_offset = 10  # 初始偏移量
    y_offset = 10  # 初始垂直偏移量（普通字符）

    for i, char in enumerate(char_list):
        # 根据字符类型选择字体
        font_to_use = font if char_type_list[i] == 'normal' else subsup_font
        # 根据字符类型调整 y_offset
        if char_type_list[i] == 'superscript':  # 上标字符
            y_offset -= subsup_font_size * 0.2  # 向上偏移
        elif char_type_list[i] == 'subscript':  # 下标字符
            y_offset += subsup_font_size * 2.0  # 向下偏移

        # 获取字符的 bounding box
        bbox = draw.textbbox((x_offset, y_offset), char, font=font_to_use)

        # 绘制字符
        draw.text((x_offset, y_offset), char, font=font_to_use, fill=(0, 0, 0))  # 黑色文字
        # 更新偏移量：字符宽度加上额外的间距
        x_offset += bbox[2] - bbox[0] + spacing  # 每个字符宽度加上spacing

        # 恢复原始 y_offset（如果上标或下标已经绘制）
        if char_type_list[i] in ['superscript', 'subscript']:
            y_offset = 10  # 恢复到原始的基线

    return image


# 获取字符的 bounding box
def get_character_bboxes(text, spacing=5):
    bboxes = []
    x_offset = 10  # 初始偏移量
    y_offset = 10  # 初始垂直偏移量（普通字符）

    # 创建一个空白图像并获取 draw 对象来计算字符尺寸
    dummy_image = Image.new("RGB", (1000, 100), (255, 255, 255))  # 预创建一个大图像
    draw = ImageDraw.Draw(dummy_image)

    char_list, char_type_list = process_text(text)

    for i, char in enumerate(char_list):
        # 根据字符类型选择字体
        font_to_use = font if char_type_list[i] == 'normal' else subsup_font
        # 根据字符类型调整 y_offset
        if char_type_list[i] == 'superscript':  # 上标字符
            y_offset -= subsup_font_size * 0.2  # 向上偏移
        elif char_type_list[i] == 'subscript':  # 下标字符
            y_offset += subsup_font_size * 2.0 # 向下偏移

        # 获取字符的 bounding box
        bbox = draw.textbbox((x_offset, y_offset), char, font=font_to_use)
        bboxes.append(bbox)
        # 更新偏移量：字符宽度加上额外的间距
        x_offset += bbox[2] - bbox[0] + spacing  # 每个字符宽度加上spacing

        # 恢复原始 y_offset（如果上标或下标已经绘制）
        if char_type_list[i] in ['superscript', 'subscript']:
            y_offset = 10  # 恢复到原始的基线

    return bboxes


# 随机生成数据
def generate_data(num_images=10, spacing=5):
    data = []

    for i in range(num_images):
        text = generate_random_text(random.randint(5, 10))  # 增加生成更长文本的概率
        print(f"Original text: {text}")  # 打印原始文本，方便对比

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
generate_data(num_images=10, spacing=5)  # 设置字符间距为 5 像素

print("生成的数据和标注已保存！")

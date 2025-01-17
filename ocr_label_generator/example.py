from PIL import Image, ImageDraw, ImageFont
import random
import string

# 设置字体和大小
font_path = "C:\\Windows\\Fonts\\arial.ttf"  # Arial 字体路径
font_size = 40
font = ImageFont.truetype(font_path, font_size)

# 设置更小的字体用于上下标
subsup_font_size = int(font_size * 0.3)  # 上下标字体为普通字体的 30%
subsup_font = ImageFont.truetype(font_path, subsup_font_size)

# 打印字体大小以确认
print(f"Normal font size: {font_size}, Subscript/Superscript font size: {subsup_font_size}")


# 根据输入生成两个列表：字符列表和字符类型标识列表
def process_text(text):
    char_list = []
    char_type_list = []  # 'normal', 'superscript', 'subscript'

    i = 0
    while i < len(text):
        if text[i] == '^':  # 上标
            char_type_list.append('superscript')
            char_list.append(text[i + 1])
            i += 2
        elif text[i] == '_':  # 下标
            char_type_list.append('subscript')
            char_list.append(text[i + 1])
            i += 2
        else:
            char_type_list.append('normal')
            char_list.append(text[i])
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
            y_offset -= subsup_font_size // 2  # 向上偏移
        elif char_type_list[i] == 'subscript':  # 下标字符
            y_offset += subsup_font_size // 2  # 向下偏移

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
    char_list, char_type_list = process_text(text)
    bboxes = []
    x_offset = 10  # 初始偏移量
    y_offset = 10  # 初始垂直偏移量（普通字符）

    # 创建一个空白图像并获取 draw 对象来计算字符尺寸
    dummy_image = Image.new("RGB", (1000, 100), (255, 255, 255))  # 预创建一个大图像
    draw = ImageDraw.Draw(dummy_image)

    for i, char in enumerate(char_list):
        # 根据字符类型选择字体
        font_to_use = font if char_type_list[i] == 'normal' else subsup_font
        # 根据字符类型调整 y_offset
        if char_type_list[i] == 'superscript':  # 上标字符
            y_offset -= subsup_font_size // 2  # 向上偏移
        elif char_type_list[i] == 'subscript':  # 下标字符
            y_offset += subsup_font_size // 2  # 向下偏移

        # 获取字符的 bounding box
        bbox = draw.textbbox((x_offset, y_offset), char, font=font_to_use)
        # 输出每个字符的bounding box
        print(f"Character: {char}, BBox: {bbox}")
        bboxes.append(bbox)
        # 更新偏移量：字符宽度加上额外的间距
        x_offset += bbox[2] - bbox[0] + spacing  # 每个字符宽度加上spacing

        # 恢复原始 y_offset（如果上标或下标已经绘制）
        if char_type_list[i] in ['superscript', 'subscript']:
            y_offset = 10  # 恢复到原始的基线

    return bboxes


# 测试输入
text_input = "EVA_23"
print(f"Processed text: {text_input}")
# 创建图像并绘制bounding box
image = create_image_with_text(text_input, spacing=5)
bboxes = get_character_bboxes(text_input, spacing=5)

# 显示图像
image.show()

# # 输出每个字符的bounding box
# for i, bbox in enumerate(bboxes):
#     print(f"Character: {text_input[i]}, BBox: {bbox}")

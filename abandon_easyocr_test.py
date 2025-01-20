import easyocr
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# 初始化阅读器，指定需要识别的语言
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

# 读取图像并进行文字识别
image_path = 'map.png'  # 替换为您的图像路径
results = reader.readtext(image_path)

# 打印识别结果
for idx, (bbox, text, prob) in enumerate(results):
    print(f'[{idx}] Text: {text}, Probability: {prob:.4f}, BBox: {bbox}')

# 可视化识别结果
# 加载图像
image = plt.imread(image_path)

# 创建绘图
fig, ax = plt.subplots(1, figsize=(image.shape[1] / 300, image.shape[0] / 300), dpi=300)
ax.imshow(image)

# 开关：是否显示编号
show_numbers = False

# 绘制识别到的文本区域
for idx, (bbox, _, _) in enumerate(results):
    # 获取边界框坐标
    polygon = Polygon(bbox, linewidth=1, edgecolor='red', facecolor='none')
    ax.add_patch(polygon)

    # 在图像上显示编号（根据开关决定）
    if show_numbers:
        top_left = bbox[0]  # 使用第一个点作为编号起始点
        plt.text(top_left[0], top_left[1] - 5, str(idx), fontsize=8, color='blue',
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# 去掉坐标轴
ax.axis('off')

# 保存结果
output_path = 'easyocr_result.png'
fig.savefig(output_path, dpi=image.shape[1] / fig.get_size_inches()[0], bbox_inches='tight', pad_inches=0.0)
print(f'Result saved to {output_path}')

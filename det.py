from paddleocr import PaddleOCR,draw_ocr
ocr = PaddleOCR(det_model_dir="model/ch_PP-OCRv4_det_server_infer", det_db_score_mode="slow") # need to run only once to download and load model into memory
img_path = 'map.png'
result = ocr.ocr(img_path, rec=False)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# draw result
from PIL import Image
result = result[0]
image = Image.open(img_path).convert('RGB')
im_show = draw_ocr(image, result, txts=None, scores=None, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

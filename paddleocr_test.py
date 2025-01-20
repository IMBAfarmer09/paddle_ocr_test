from paddleocr import PaddleOCR, draw_ocr

# Paddleocr supports Chinese, English, French, German, Korean and Japanese
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order
ocr = PaddleOCR(use_angle_cls=True,
                det_model_dir="model/ch_PP-OCRv4_det_server_infer",
                rec_model_dir="model/ch_PP-OCRv4_rec_server_infer",
                cls_model_dir="model/ch_ppocr_mobile_v2.0_cls_slim_infer",
                det_max_side_len=2000,
                det_db_score_mode="slow") # need to run only once to download and load model into memory
# img_path = 'PaddleOCR/doc/imgs_en/img_12.jpg'
img_path = 'map.png'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# draw result
from PIL import Image
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
txts = None
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/fonts/simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('paddleocr_result.png')
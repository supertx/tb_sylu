"""
@author: supermantx
@time: 2021/11/17 14:48
paddleOCR的简易模型识别效果不是很好(deprecate)
"""
from paddleocr import PaddleOCR

ocr = PaddleOCR()
n = ocr.ocr("123.jpeg", det=False)
code = n[0][0].code(' ', '')

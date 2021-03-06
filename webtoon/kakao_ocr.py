import json
import os

import cv2
import requests
import sys

from kakaotrans import Translator

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40

KAKAO_LANGUAGE_DICT = {'English': 'en', 'Japanese': 'jp', 'chinese': 'cn', 'vietnamese': 'vi',
                       'Indonesia': 'id', 'arabic': 'ar', 'Bengal': 'bn', 'german': 'de',
                       'spanish': 'es', 'french': 'fr', 'Hindi': 'hi', 'italian': 'it',
                       'malaysian': 'ms', 'dutch': 'nl', 'portukal ': 'pt', 'russian': 'ru',
                       'thai': 'th', 'turkish': 'tr'}


def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    print("image: ", image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})

def kakao_translator(text: str, target: str):
    translator = Translator()
    result = translator.translate(text, src="kr", tgt=target, separate_lines=True)
    return result

import json, sys, os
from collections import OrderedDict

import numpy as np

from kakao_ocr import kakao_ocr_resize, kakao_ocr, kakao_translator
from opencv_cut import json_load, opencv_cut, bubble_xy

# opencv를 사용하여 말풍선 이미지를 따로 저장
def opencv_cut_main(i):
    bubbles = json_load(i)
    min_max_list = bubble_xy(bubbles)
    extension = i.find(".")  # 확장자는 .txt, .jpg이런 형식이므로 .을 찾음 여기서는 .이 있는 인덱스 번호 출력
    convert = i[:extension + 1] + 'jpg'  # 파일 이름 저장!
    cnt = 1
    for j in min_max_list:
        save_name = i[:extension] + "_" + str(cnt) + '.jpg'  # 파일 이름 저장!
        opencv_cut(j[0], j[1], j[2], j[3], convert, save_name)
        cnt += 1

def kakao_ocr_main(image_path: str):
    if len(sys.argv) != 3:  # 환경변수
        print("Please run with args: $ python example.py /path/to/image appkey")

        appkey='4d21228a249b7f6fb6b88dfe9b06ac7e'
        resize_impath = kakao_ocr_resize(image_path)

        if resize_impath is not None:
            image_path = resize_impath
            print("원본 대신 리사이즈된 이미지를 사용합니다.")

        output = kakao_ocr(image_path, appkey).json()
        # print("[OCR] output:\n{}\n".format(json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False)))
        return output


# 카카오 ocr로 나온 text 데이터를 한 줄로 묶는 과정
# 텍스트 박스 좌표 지정
def text_recongition_words(ocr_data: dict):
    tmp_text = []
    tmp_box = []
    for i in range(len(ocr_data["result"])):
        tmp_text.append(ocr_data["result"][i]["recognition_words"][0])
        for j in range(len(ocr_data["result"][i]["boxes"])):
            tmp_box.append(ocr_data["result"][i]["boxes"][j])
    result_text = " ".join(tmp_text)

    if len(tmp_box) > 1:
        tmp_box = np.array(tmp_box)
        boxes_min = np.min(tmp_box, axis=0)
        boxes_max = np.max(tmp_box, axis=0)
    else:
        return None, None, None

    print("번역 : ", result_text)
    print("최소 좌표 : ", boxes_min)
    print("최대 좌표 : ", boxes_max)

    return result_text, boxes_min, boxes_max



def main():

    for i in os.listdir('../temp/json/'):
        opencv_cut_main(i)

    for i in os.listdir('../temp/trim/'):
        output = kakao_ocr_main('../temp/trim/' + i)
        result_text, boxes_min, boxes_max = text_recongition_words(output)





if __name__ == "__main__":
    main()

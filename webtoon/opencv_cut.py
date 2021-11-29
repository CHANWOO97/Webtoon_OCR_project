import cv2
import json

from matplotlib import pyplot as plt
import numpy as np

# 1. json 파일 불러오기 및 bubble 좌표값 가져오기
def json_load(i):
    path = '../temp/json/'+i
    with open(path, 'r')as f:
        json_data = json.load(f)
    # print(json.dumps(json_data, indent="\t"))

    shapes = json_data['shapes']

    bubbles = []
    for idx, data in enumerate(shapes):  # print(idx, data['label'])
        if 'bubble' in data['label']:
            bubbles.append(data['points'])
            # print(*bubbles, sep='\n')

    return bubbles


# image json 좌표값 함수
def bubble_xy(bubbles):
    min_max_list = []
    for i in bubbles:
        bubble_x = []
        bubble_y = []
        for x, y in i:
            bubble_x.append(x)
            bubble_y.append(y)
            x_max = int(max(bubble_x))
            x_min = int(min(bubble_x))
            y_max = int(max(bubble_y))
            y_min = int(min(bubble_y))

        min_max_list.append([x_max, x_min, y_max, y_min])

    return min_max_list


# image trim 하기
def opencv_cut(x_max, x_min, y_max, y_min, convert, save_name):
    x = x_min
    y = y_min
    w = x_max-x_min
    h = y_max-y_min

    path_1 = '../temp/media/'+convert
    path_2 = '../temp/trim/'

    image = cv2.imread(path_1)

    img_trim = image[y:y+h, x:x+w]
    cv2.imwrite(path_2 + f'trim_{save_name}', img_trim)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






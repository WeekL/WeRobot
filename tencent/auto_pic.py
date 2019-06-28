import base64
import random
import string
import time

import requests

from data import api
from tencent import api_auth, auto_text
from utils import file_util


def image_recognition(image_path):
    # 图像识别的API地址 
    url = "https://api.ai.qq.com/fcgi-bin/vision/vision_imgtotext"
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 图片base64编码
    f = open(image_path, 'rb')
    image_data = f.read()
    data = base64.b64encode(image_data)  # 得到 byte 编码的数据

    params = {'app_id': api.app_id,
              'image': data,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              'session_id': '10000'
              }
    params['sign'] = api_auth.get_req_sign(params)
    r = requests.post(url, data=params)
    answer = r.json()["data"]["text"]
    if not answer:
        print(r.json())
        return '哦吼～出了点小问题，请“呼叫本人”'
    else:
        return answer


def get_content(image_path):
    # 获取请求参数  
    image_path = image_path.encode('utf-8')
    r_img = image_recognition(image_path)
    print(r_img)
    answer = auto_text.get_content(r_img)
    file_util.delete_file(image_path)
    return answer

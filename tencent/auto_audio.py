import base64
import random
import string
import time

import requests

from tencent import api_auth, auto_text
from utils import audio_util


def speech_recognition(audio_path):
    # 语音识别的API地址 
    url = "https://api.ai.qq.com/fcgi-bin/aai/aai_asr"
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 音频base64编码
    f = open(audio_path, 'rb')
    audio_data = f.read()
    data = base64.b64encode(audio_data)  # 得到 byte 编码的数据
    params = {'app_id': api_auth.app_id,
              'speech': data,
              'format': '2',
              'rate': '16000',
              'time_stamp': time_stamp,
              'nonce_str': nonce_str
              }
    params['sign'] = api_auth.get_req_sign(params)
    r = requests.post(url,data=params)
    txt = r.json()['data']['text']
    if not txt:
        return '哦吼～出了点小问题，请“呼叫本人”'
    else:
        return txt


def speech_synthesis(txt):
    # 语音合成api
    url = 'https://api.ai.qq.com/fcgi-bin/aai/aai_tta'
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))

    params = {'app_id': api_auth.app_id,
              'text': txt,
              'model_type': 2,
              'speed': 0,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str
              }
    params['sign'] = api_auth.get_req_sign(params)
    return requests.get(url, data=params)


def get_reply(audio_path):
    # 获取请求参数  
    audio_path = audio_path.encode('utf-8')
    # 获取语音识别结果
    r_recognition = speech_recognition(audio_path)
    print(r_recognition)
    # 获取回复文字
    r_txt = auto_text.get_content(r_recognition)
    # print(r_txt)
    # 获取语音合成结果
    # r_synthesis = speech_synthesis(r_txt)
    # answer = r_synthesis.json()["data"]["voice"]
    answer = r_txt
    if not answer:
        # print(r_synthesis.json())
        return '哦吼～出了点小问题，请“呼叫本人”'
    else:
        # return audio_util.base642mp3(answer)
        return answer

import time
import random
import string
import requests

from data import api
from tencent import api_auth


def get_params(receive_text):
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    params = {'app_id': api.app_id,
              'question': receive_text,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              'session': '10000'
              }
    params['sign'] = api_auth.get_req_sign(params)
    return params


def get_content(plus_item):
    global payload, r
    # 聊天的API地址 
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    # 获取请求参数  
    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item)
    # r = requests.get(url,params=payload)  
    r = requests.post(url, data=payload)
    answer = r.json()["data"]["answer"]
    if not answer:
        print(r.json())
        return '哦吼～出了点小问题，请“呼叫本人”'
    else:
        return answer


def get_sentiments(comments):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar"
    comments = comments.encode('utf-8')
    payload = get_params(comments)
    r = requests.post(url, data=payload)
    return r.json()

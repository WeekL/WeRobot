import base64
import json

from aip import AipSpeech
import requests

from data.api import APP_ID, API_KEY, SECRET_KEY
from utils.file_util import get_file_content, get_file_size

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_token():
    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}' \
        .format(API_KEY, SECRET_KEY)
    r = requests.post(url)
    return r.json()['access_token']


def get_result(file):
    url = 'https://vop.baidu.com/server_api'
    speech_data = base64.b64encode(get_file_content(file))
    params = json.dumps({
        "format": str.split(file, '.')[1],
        "rate": "16000",
        "dev_pid": "1536",
        "channel": "1",
        "token": get_token(),
        "cuid": "weRobot",
        "len": get_file_size(file),
        "speech": str(speech_data, encoding='utf-8')
    })
    r_json = requests.post(url, data=params).json()
    if not r_json['err_no'] == 0:
        print('err_no:{}, err_msg:{}'.format(r_json['err_no'], r_json['err_msg']))
        return '哦吼～出了点小问题，请“呼叫本人”'
    else:
        return r_json['result'][0]

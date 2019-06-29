import base64

import time
from pydub import AudioSegment

from utils import file_util


def mp32wav(path, file_name, frame_rate=16000):
    # from_path: 目标音频文件路径
    # to_path: 转码后文件路径
    # frame_rate: 默认16kHz，可以frame_rate=8000，既8kHz
    AudioSegment.converter = '{}ffmpeg.exe'.format(file_util.get_root_path())
    name = str.split(file_name, '.')[0]
    mp3_file = path + file_name
    print(mp3_file)
    mp3_version = AudioSegment.from_mp3(mp3_file)  # 可以根据文件不太类型导入不同from方法
    # ogg_version = AudioSegment.from_ogg("never_gonna_give_you_up.ogg")
    # flv_version = AudioSegment.from_flv("never_gonna_give_you_up.flv")
    mono = mp3_version.set_frame_rate(frame_rate).set_channels(1)  # 设置声道和采样率
    result = path + name + '.wav'
    mono.export(result, format='wav', codec='pcm_s16le')  # codec此参数本意是设定16bits pcm编码器, 但发现此参数可以省略
    return result


def base642mp3(base64_data):
    t = time.time()
    file = "{}audio\\{}.mp3".format(file_util.get_root_path(), t)
    ori_image_data = base64.b64decode(base64_data)
    fout = open(file, 'wb')
    fout.write(ori_image_data)
    fout.close()
    return file

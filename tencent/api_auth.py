# 签名算法：
# 1. 计算步骤
# 将<key, value>请求参数对按key进行字典升序排序，得到有序的参数对列表N
# 将列表N中的参数对按URL键值对的格式拼接成字符串，得到字符串T（如：key1=value1&key2=value2），URL键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8，而不是小写%e8
# 将应用密钥以app_key为键名，组成URL键值拼接到字符串T末尾，得到字符串S（如：key1=value1&key2=value2&app_key=密钥)
# 对字符串S进行MD5运算，将得到的MD5值所有字符转换成大写，得到接口请求签名
#
# 2. 注意事项
# 不同接口要求的参数对不一样，计算签名使用的参数对也不一样
# 参数名区分大小写，参数值为空不参与签名
# URL键值拼接过程value部分需要URL编码
# 签名有效期5分钟，需要请求接口时刻实时计算签名信息

from urllib import parse
import hashlib

from data.api import app_key


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()


def get_req_sign(params):
    sign_before = ''
    # 要对key排序再拼接
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
        value = parse.quote(params[key], safe='')
        value = value.replace('%20', '+').replace('~', '%7E')
        if key == 'question':
            print(value)
        sign_before += '{}={}&'.format(key, value)
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名  
    sign = curlmd5(sign_before)
    return sign

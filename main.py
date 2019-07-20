import re

import itchat
import time

import os
from itchat.content import *
from tencent import auto_text, auto_pic, auto_audio
import utils.file_util as fu
import utils.audio_util as au

msg_information = {}
face_bug = None  # 针对表情包的内容


def need_reply(remark_name):
    if u'#1' in remark_name:
        return True
    else:
        return False


@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    global face_bug
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 接受消息的时间
    msg_from = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']  # 在好友列表中查询发送信息的好友昵称
    msg_time = msg['CreateTime']  # 信息发送的时间
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐

    tag = need_reply(msg_from)

    msg_type = msg['Type']
    reply = None
    if msg_type == 'Text':
        msg_content = msg['Text']
        receive = str.replace(msg['Text'], "\\", "/")
        if tag:
            if u'呼叫本人' == receive.strip():
                reply = u"正在招魂～请稍等..."
            else:
                reply = u"{}".format(auto_text.get_content(receive))
    elif msg_type == 'Picture':
        pic_path = fu.get_root_path() + 'data\\image\\'  # 图片保存路径
        msg['Text'](fu.comfirm_dir(pic_path) + msg['FileName'])
        msg_content = pic_path + msg['FileName']
        if tag:
            if fu.get_file_size(pic_path + msg['FileName']) > 1024 * 1024:  # 只识别1Mb以下的图片
                print('{}大于1Mb，不处理'.format(msg['FileName']))
            elif str.split(msg['FileName'], '.')[1] == 'gif':  # 只识别静态图片
                print('{}是动态图片，不处理'.format(msg['FileName']))
            else:
                reply = auto_pic.get_content(pic_path + msg['FileName'])
    elif msg_type == 'Recording':
        audio_path = fu.get_root_path() + 'data\\audio\\'  # 语音保存路径
        msg['Text'](fu.comfirm_dir(audio_path) + msg['FileName'])
        msg_content = audio_path + msg['FileName']
        if tag:
            reply = auto_audio.get_reply(au.mp32wav(audio_path, msg['FileName']))
    elif msg_type == 'Video':
        video_path = fu.get_root_path() + 'data\\video\\'
        msg['Text'](fu.comfirm_dir(video_path) + msg['FileName'])
        msg_content = video_path + msg['FileName']
        if tag:
            reply = '啥？视频？'
    elif msg_type == 'Attachment':
        attach_path = fu.get_root_path() + 'data\\attach\\'
        msg['Text'](fu.comfirm_dir(attach_path) + msg['FileName'])
        msg_content = attach_path + msg['FileName']
        if tag:
            reply = '让我看看是啥...我擦，8个G的葫芦娃'
    elif msg_type == "Map":
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()  # 内容为详细的地址
        else:
            msg_content = r"" + location
    elif msg_type == 'Card':
        msg_content = msg['Text']['NickName'] + '的名片'
        if msg['Text']['Sex'] == 1:
            msg_content += '，性别为男'
        else:
            msg_content += '，性别为女'
        if tag:
            reply = u'收到好友名片：{}'.format(msg_content)
    elif msg_type == 'Sharing':
        msg_content = msg['Text']
        msg_share_url = msg['Url']  # 记录分享的url
        if tag:
            reply = u'收到分享' + msg['Text']

    # 将信息存储在字典中，每一个msg_id对应一条信息
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )
    if tag and reply is not None:
        return reply


# 防撤回
@itchat.msg_register(NOTE)
def anti_withdrawal(msg):
    # 这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)  # 在返回的content查找撤回的消息的id
        old_msg = msg_information.get(old_msg_id)  # 得到消息
        print(old_msg)
        if len(old_msg_id) < 11:  # 如果发送的是表情包
            itchat.send_file(face_bug, toUserName='filehelper')
        else:  # 发送撤回的提示给文件助手
            content = u"" + old_msg.get('msg_content')
            if os.path.split(content):
                content = os.path.split(content)[1]
            msg_body = "告诉你一个秘密~" + "\n" \
                       + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "撤回内容：\n" + content
            # 如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

            # 将撤回消息发送到文件助手
            itchat.send_msg(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            # 删除相应文件
            fu.delete_file(old_msg.get('msg_content'))
            # 删除字典旧消息
            msg_information.pop(old_msg_id)


if __name__ == '__main__':
    # itchat.auto_login(hotReload=True, statusStorageDir='newInstance.pkl')
    itchat.auto_login(hotReload=False, enableCmdQR=2)
    # itchat.auto_login(hotReload=True)

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run(debug=True)

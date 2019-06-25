import itchat

import tencent.auto_pic
import tencent.auto_text
from util.file_utils import get_root_path, get_file_size


@itchat.msg_register('Text')
def text_reply(msg):
    user_name = msg['FromUserName']
    itchat.search_mps
    # receive = str.strip(msg['Text'])
    receive = str.replace(msg['Text'], "\\", "/")
    if u'呼叫本人' in receive:
        return u"正在招魂～请稍等..."
    else:
        return u"{}".format(tencent.auto_text.get_content(receive))


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def attach_reply(msg):
    reply = '处理中，请稍后。。。'
    if msg['Type'] == 'Picture':
        pic_path = get_root_path() + 'data\\image\\'  # 图片保存路径
        msg['Text'](pic_path + msg['FileName'])
        if not get_file_size(pic_path + msg['FileName']) > 1024 * 1024:  # 只识别1Mb以下的图片
            return tencent.auto_pic.get_content(pic_path + msg['FileName'])
        else:
            print('{}大于1Mb，不处理'.format(msg['FileName']))
    elif msg['Type'] == 'Recording':
        audio_path = get_root_path() + 'data\\audio\\'  # 语音保存路径
        msg['Text'](audio_path + msg['FileName'])
        print(msg)
        pass
    elif msg['Type'] == 'Video':
        reply = '啥？视频？'
    elif msg['Type'] == 'Attachment':
        reply = '让我看看是啥...我擦，8个G的葫芦娃'
    return reply
    # return u"[自动回复]{}".format(tuling_attach(msg[msg['Type']]))
    # return (u'[自动回复]' + {'Picture': u'图片', 'Recording': u'录音', 'Attachment': u'附件', 'Video': u'视频'}
    #         .get(msg['Type']) + u'已下载到本地')  # download function is: msg['Text'](msg['FileName'])


@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    print(msg)
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友名片：' + msg['Text']['NickName']


if __name__ == '__main__':
    # itchat.auto_login(hotReload=True, statusStorageDir='newInstance.pkl')
    itchat.auto_login(hotReload=True)

    # 获取自己的UserName
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run(debug=True)

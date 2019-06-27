import itchat
from tencent import auto_text, auto_pic, auto_audio
import utils.file_util as fu
import utils.audio_util as au


@itchat.msg_register('Text')
def text_reply(msg):
    user_name = msg['FromUserName']
    itchat.search_mps
    # receive = str.strip(msg['Text'])
    receive = str.replace(msg['Text'], "\\", "/")
    if u'呼叫本人' in receive:
        return u"正在招魂～请稍等..."
    else:
        return u"{}".format(auto_text.get_content(receive))


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def attach_reply(msg):
    reply = '处理中，请稍后。。。'
    if msg['Type'] == 'Picture':
        pic_path = fu.get_root_path() + 'data\\image\\'  # 图片保存路径
        msg['Text'](fu.comfirm_dir(pic_path) + msg['FileName'])
        if fu.get_file_size(pic_path + msg['FileName']) > 1024 * 1024:  # 只识别1Mb以下的图片
            print('{}大于1Mb，不处理'.format(msg['FileName']))
        elif str.split(msg['FileName'], '.')[1] == 'gif':
            print('{}是动态图片，不处理'.format(msg['FileName']))
        else:
            return auto_pic.get_content(pic_path + msg['FileName'])
    elif msg['Type'] == 'Recording':
        audio_path = fu.get_root_path() + 'data\\audio\\'  # 语音保存路径
        msg['Text'](fu.comfirm_dir(audio_path) + msg['FileName'])
        return auto_audio.get_reply(au.mp32wav(audio_path, msg['FileName']))
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

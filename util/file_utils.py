import os


def get_root_path():
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("itChatTest\\") + len("itChatTest\\")]  # 获取itChatTest根路径
    return rootPath

def get_file_size(path):
    return os.path.getsize(path)

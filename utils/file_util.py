import os


def get_root_path():
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("WeRobot\\") + len("WeRobot\\")]  # 获取WeRobot根路径
    return rootPath


def get_file_content(path):
    with open(path, 'rb') as fp:
        return fp.read()


def get_file_size(path):
    return os.path.getsize(path)


def comfirm_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

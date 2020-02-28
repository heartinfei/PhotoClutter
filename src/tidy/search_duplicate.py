#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import hashlib
from src.tidy.support_types import *

# 等价Map， md5 --> path
filter_dict = {}

print("当前OS：" + os.name)

support_types = []

support_types.extend(video_types)
support_types.extend(img_types)


def find_duplicate_files_in_dir(target_dir):
    """
    获取当前目录以及子目录下的所有照片文件
    :param target_dir: 扫描目录
    :return: [0] 重复文件，[1] 非重复文件
    """
    duplicate_photos = []
    un_duplicate_photos = []
    for entry in os.scandir(target_dir):
        file_name: str = entry.name
        file_path = entry.path
        if file_name.startswith("."):
            continue
        elif file_name.endswith(".photoslibrary"):
            continue
        elif os.path.isdir(file_path):
            result = find_duplicate_files_in_dir(file_path)
            duplicate_photos.extend(result[0])
            un_duplicate_photos.extend(result[1])
        else:
            suffix = get_file_suffix(file_name)
            if suffix is None or suffix not in support_types:
                # 无后缀名的文件不处理
                print("{}不支持文件不进行处理 ".format(file_path))
                continue

            _md5 = _get_img_md5(file_path)
            if _md5 in filter_dict:
                print("找到重复文件：{}".format(file_path))
                duplicate_photos.append(file_path)
            else:
                filter_dict[_md5] = file_path
                un_duplicate_photos.append(file_path)

    return duplicate_photos, un_duplicate_photos


def _is_duplicate(img_file):
    """
    判断文件是否存在，如果存在返回None，否则返回md5
    :param img_file:
    :return:
    """
    _md5 = _get_img_md5(img_file)
    if _md5 in filter_dict:
        return None
    else:
        return _md5


def _get_img_md5(img_file):
    return hashlib.md5(open(img_file, 'rb').read()).hexdigest()


if __name__ == "__main__":
    # 启动脚本
    test_dir = "/Users/smzdm/Public/ImgSource"
    d_files = find_duplicate_files_in_dir(test_dir)
    log = open("{}/dup_{}.log".format(test_dir, len(d_files)), "w")
    for f in d_files[0]:
        log.write(f + "\n")
    log.close()
    print(d_files)

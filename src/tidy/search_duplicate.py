#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import hashlib

# 等价Map， md5 --> path
filter_dict = {}

print("当前OS：" + os.name)


def handle_target_dir(photo_dir):
    return filter_photos_in_dir(photo_dir, handle_photo)


def filter_photos_in_dir(photo_dir, handle_fun):
    """
    获取当前目录以及子目录下的所有照片文件
    :param photo_dir: 扫描目录
    :param handle_fun:
    :return: 照片文件集合
    """
    duplicate_photos = []
    for element in os.listdir(photo_dir):
        if element.startswith("."):
            continue
        _full_name = os.path.join(photo_dir, element)
        if os.path.isdir(_full_name) and not _full_name.endswith(".photoslibrary"):
            duplicate_photos.extend(filter_photos_in_dir(_full_name, handle_fun))
        elif _full_name.endswith(".jpeg") and handle_fun(photo_dir, _full_name):
            duplicate_photos.append(_full_name)
        elif _full_name.endswith(".png"):
            duplicate_photos.append(_full_name)
    return duplicate_photos


def handle_photo(d, img):
    """
    处理Photo File如果文件重复返回true，
    非重复文件将文件添加到全局去重字典，返回false
    :param d: 文件夹
    :param img: 文件名
    :return:
    """
    _photo_file = os.path.join(d, img)
    _md5 = is_duplicate(_photo_file)
    if _md5 is None:
        return True
    else:
        filter_dict[_md5] = _photo_file
        return False


def is_duplicate(img_file):
    """
    判断文件是否存在，如果存在返回None，否则返回md5
    :param img_file:
    :return:
    """
    _md5 = get_img_md5(img_file)
    if _md5 in filter_dict:
        return None
    else:
        return _md5


def get_img_md5(img_file):
    return hashlib.md5(open(img_file, 'rb').read()).hexdigest()


if __name__ == "__main__":
    # 启动脚本
    d_files = filter_photos_in_dir(input("请输入文件目录："), handle_photo)
    log = open("/Users/smzdm/dup_{}.log".format(len(d_files)), "w")
    for f in d_files:
        log.write(f + "\n")
    log.close()
    print(d_files)

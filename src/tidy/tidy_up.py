#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from src.tidy.rename_file import rename_all_files_in_dir
from src.tidy.search_duplicate import *


def move_files_to_target_dir(file_path: str, dst: str):
    """
    将文件移动到指定目录
    :param file_path:
    :param dst:
    :return:
    """
    if not os.path.exists(dst):
        os.mkdir(dst)
    if not os.path.isdir(file_path):
        file_name = os.path.split(file_path)[1]
        new_path = os.path.join(dst, file_name)
        shutil.move(file_path, new_path)
        print("移动文件：{}-->{}".format(file_path, new_path))


def del_empty_dir(dir_path: str):
    """
    尝试删除文件夹，如果文件为空则删除
    :param dir_path: 文件夹路径
    :return:
    """
    for entry in os.scandir(dir_path):
        _path = entry.path
        if os.path.isdir(_path):
            del_empty_dir(_path)

    try:
        os.rmdir(dir_path)
    except NotImplementedError:
        pass
    except OSError:
        pass


def flat_move_to_target_dir(src, dst):
    """
    将目标文件夹（src）及子文件夹中的所有文件移动到dst文件夹
    :param src: 源文件夹
    :param dst: 目标文件夹（存放整理后的内容）
    :return: None
    """
    for entry in os.scandir(src):
        file_name = entry.name
        file_path = entry.path
        if file_name.startswith(".") or file_name.endswith(".photoslibrary"):
            continue
        if os.path.isdir(file_path):
            flat_move_to_target_dir(file_path, dst)
            continue
        if not os.path.exists(dst):
            os.mkdir(dst)
        shutil.move(file_path, os.path.join(dst, file_name))


if __name__ == "__main__":
    source_dir = "/Volumes/SSD256/export"
    clutter_dir = "/Volumes/SSD256/clutter"
    duplicate_dir = "/Volumes/SSD256/duplicated"
    # # 重命名所有文件
    rename_all_files_in_dir(source_dir)
    # # 搜索结果
    # search_result = find_duplicate_files_in_dir(source_dir)
    # duplicate_files = search_result[0]
    # # 重复文件存放到指定目录
    # for f in duplicate_files:
    #     move_files_to_target_dir(f, duplicate_dir)
    # clutter_files = search_result[1]
    # # 非重复文件存放到指定目录
    # for c in clutter_files:
    #     move_files_to_target_dir(c, clutter_dir)
    #
    # flat_move_to_target_dir(source_dir, clutter_dir)
    # 删除空目录
    # del_empty_dir(source_dir)
    # TODO 视频文件去重 & Live Photo处理 &



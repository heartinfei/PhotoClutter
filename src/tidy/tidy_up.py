#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from src.tidy.rename_file import *
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


def flat_move_live_phone_to_target_dir(src, dst):
    """
    将Live Photo移动到指定目录，Live Phone是由两个文件组成的，在移动的过程中逻辑有所不同
    :param src: 源文件夹
    :param dst: 存放整理结果整理文件夹
    :return: None
    """
    for entry in os.scandir(src):
        heic_file_name = entry.name
        heic_file_path = entry.path
        if heic_file_name.startswith("."):
            continue
        if os.path.isdir(heic_file_path):
            flat_move_live_phone_to_target_dir(heic_file_path, dst)
            continue
        if get_file_suffix(heic_file_name) != ".heic":
            continue

        mov_file_path = os.path.splitext(heic_file_path)[0] + ".mov"
        if not os.path.exists(mov_file_path):
            continue
        mov_file_name = heic_file_name[:-5] + ".mov"
        if not os.path.exists(dst):
            os.mkdir(dst)

        shutil.move(heic_file_path, os.path.join(dst, heic_file_name))
        shutil.move(mov_file_path, os.path.join(dst, mov_file_name))


if __name__ == "__main__":
    source_dir = "/Volumes/SSD256/videos"
    clutter_dir = "/Volumes/SSD256/clutter"
    duplicate_dir = "/Volumes/SSD256/duplicated"
    # 重命名Live Photo
    print("开始重命名文件")
    # rename_live_photo_in_dir(source_dir)
    rename_all_files_in_dir(source_dir)
    print("开始整理文件")
    flat_move_to_target_dir(source_dir, clutter_dir)
    # flat_move_live_phone_to_target_dir(source_dir, clutter_dir)
    # # 重命名所有文件
    # rename_all_files_in_dir(source_dir)
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
    print("开始删除空文件夹")
    del_empty_dir(source_dir)
    # TODO 视频文件去重 & Live Photo处理 &

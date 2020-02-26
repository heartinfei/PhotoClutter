#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from src.tidy.extract_exif_as_fname import rename_file_in_dir
from src.tidy.search_duplicate import *


def empty_target(log_file: str):
    """
    删除log文件中记录的文件
    :param log_file:
    :return:
    """
    for line in open(log_file, "r").readline():
        try:
            os.remove(line)
        except NotImplementedError:
            print("tidy_up-->NotImplementedError")


def del_by_list(file_list: list):
    """
    删除列表里的文件
    :param file_list:
    :return:
    """
    for path in file_list:
        try:
            os.remove(path)
        except NotImplementedError:
            print("tidy_up-->NotImplementedError")


def move_to_target_dir(src, dst):
    for element in os.listdir(src):
        full_name = os.path.join(src, element)
        if full_name.startswith(".") or full_name.endswith(".photoslibrary"):
            continue
        if os.path.isdir(full_name):
            move_to_target_dir(full_name, dst)
        if full_name.endswith(".jpeg"):
            if not os.path.exists(dst):
                os.mkdir(dst)
            shutil.move(full_name, os.path.join(dst, element))


if __name__ == "__main__":
    target_dir = input("请输入文件目录：")
    result_list = handle_target_dir(target_dir)
    del_by_list(result_list)
    rename_file_in_dir(target_dir)
    move_to_target_dir(target_dir, "/Users/smzdm/imgs_new")

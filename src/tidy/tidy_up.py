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
        file_name = os.path.split(file_path)
        shutil.move(file_path, os.path.join(dst, file_name))


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


def search_duplicate_file():
    result = find_duplicate_files_in_dir(input("请输入文件目录："))
    log_path = input("请输入结果保存路径：")
    log_file = open(log_path + ".log", "rw")
    for r in result:
        log_file.write(r + "\n")
    log_file.close()
    print("搜索结果保存在 {}".format(log_path))


def rename_all_file_in_target_dir():
    rename_all_files_in_dir(input("请输入文件目录："))


def flat_dir():
    flat_move_to_target_dir(input("请输入待整理文件目录："), input("请输入存放整理结果目录："))


def auto_tidy_up():
    """
    自动整理文件夹
    :return:
    """
    src_dir = input("请输入文件目录：")
    duplicate_dir = input("输入重复文件目录：")
    dst_dir = input("请输入存放整理结果目录：")
    result_list = find_duplicate_files_in_dir(src_dir)
    move_files_to_target_dir(result_list, duplicate_dir)
    # del_by_list(result_list)
    # rename_file_in_dir(src_dir)
    flat_move_to_target_dir(src_dir, dst_dir)


def default():
    print("No such command.")


if __name__ == "__main__":
    tips = """
    *********************************
    * 1. 搜索重复文件
    * 2. 重命名文件
    * 3. 文件夹子目录展平
    * 4. 智能整理文件夹（1 & 2 & 3）
    *********************************
    """
    print(tips)
    # cmd = input("请输入功能索引：")
    switch = {"1": search_duplicate_file,
              '2': rename_all_file_in_target_dir,
              '3': flat_dir,
              '4': auto_tidy_up}

    # switch.get(cmd, default)()

    test_path = "/Users/smzdm/Public/ImgSource"
    target_dir = "/Users/smzdm/clutter"
    flat_move_to_target_dir(test_path, target_dir)
    # del_empty_dir(test_path)
    # for p in os.listdir(test_path):
    #     print(p)

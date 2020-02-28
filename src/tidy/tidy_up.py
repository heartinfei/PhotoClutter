#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from src.tidy.rename_file import rename_files_in_dir
from src.tidy.search_duplicate import *


def del_file_by_log_record(log_file: str):
    """
    删除log文件中记录的文件
    :param log_file:
    :return:
    """
    for line in open(log_file, "r").readline():
        try:
            os.scandir()
            os.remove(line)
        except NotImplementedError:
            print("tidy_up-->NotImplementedError")


def del_file_by_list(file_list: list):
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


def move_files_to_target_dir(fs: list, dst: str):
    index = 0
    for f_path in fs:
        if not os.path.exists(dst):
            os.mkdir(dst)
        fname = os.path.split(f_path)[1]
        if fname is None:
            continue
        index = index + 1
        fname = str(index) + fname
        shutil.move(f_path, os.path.join(dst, fname))


def del_empty_dir(dir_path: str):
    """
    尝试删除文件夹，如果文件为空则删除
    :param dir_path: 文件夹路径
    :return:
    """
    try:
        os.rmdir(dir_path)
    except NotImplementedError or OSError:
        pass


def flat_move_to_target_dir(src, dst):
    """
    将目标文件夹（src）及子文件夹中的所有文件移动到dst文件夹
    :param src: 源文件夹
    :param dst: 目标文件夹（存放整理后的内容）
    :return: None
    """
    for element in os.listdir(src):
        full_name = os.path.join(src, element)
        if full_name.startswith(".") or full_name.endswith(".photoslibrary"):
            continue
        if os.path.isdir(full_name):
            flat_move_to_target_dir(full_name, dst)
        if not os.path.exists(dst):
            os.mkdir(dst)
        shutil.move(full_name, os.path.join(dst, element))


def search_duplicate_file():
    result = handle_target_dir(input("请输入文件目录："))
    log_path = input("请输入结果保存路径：")
    log_file = open(log_path + ".log", "rw")
    for r in result:
        log_file.write(r + "\n")
    log_file.close()
    print("搜索结果保存在 {}".format(log_path))


def rename_all_file_in_target_dir():
    pass
    # rename_files_in_dir(input("请输入文件目录："))


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
    result_list = handle_target_dir(src_dir)
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
    # for p in os.listdir(test_path):
    #     print(p)
    for entry in os.scandir(test_path):
        file_name = entry.name
        path = entry.path
        print(file_name)

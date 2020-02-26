#!/usr/bin/python3
# -*- coding: utf-8 -*-

import exifread
import os
import datetime


def rename_file_in_dir(d):
    """
    重命名照片
    :param d: 目录
    :return: None
    """
    for element in os.listdir(d):
        f_name = os.path.join(d, element)
        if not element.endswith(".jpeg"):
            continue
        elif os.path.isdir(f_name):
            rename_file_in_dir(f_name)
            break
        else:
            img = open(f_name, "rb")
            tags = exifread.process_file(img)
            now = datetime.datetime.now()
            shot_time = tags.get('EXIF DateTimeOriginal', now)
            make = tags.get('Image Make', "unknow")
            model = tags.get('Image Model', 'unknow')
            new_name = "{}_{}_{}.jpeg".format(shot_time, make, model).replace(" ", "_")
            new_path = os.path.join(d, new_name)
            try:
                os.rename(f_name, new_path)
            except NotImplementedError:
                print("extract_exif_as_fname-->NotImplementedError")


if __name__ == "__main__":
    print("作为模块倒入的时候不执行！")
    clutter_path = input("输入批处理文件名：")
    rename_file_in_dir(clutter_path)

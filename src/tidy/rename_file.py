#!/usr/bin/python3
# -*- coding: utf-8 -*-

import exifread
import datetime
from src.tidy.support_types import *
from moviepy.editor import VideoFileClip


def rename_all_files_in_dir(target_dir):
    """
    重命名文件夹中的所有文件
    :param target_dir: 目录
    :return: None
    """
    for entry in os.scandir(target_dir):
        file_name = entry.name
        print("处理文件{}".format(file_name))
        if file_name.startswith("."):
            # 系统隐藏文件/文件夹不处理
            continue
        file_path = entry.path
        if os.path.isdir(file_path):
            rename_all_files_in_dir(file_path)
            continue
        else:
            suffix = get_file_suffix(file_name)
            if suffix is None:
                # 无后缀名的文件不处理
                print("{}无后缀名不进行处理 ".format(file_path))
                continue
            if len(suffix.strip()) == 0:
                continue
            new_name = ""

            if suffix in img_types:
                # 对照片重命名
                new_name = gen_name_for_img(file_path) + suffix
            elif suffix in video_types:
                # 对视频文件重命名
                new_name = gen_name_for_video(file_path) + suffix
            else:
                continue

            # 合成新路径
            new_file_path = os.path.join(target_dir, new_name)
            if not rename_file(file_path, new_file_path):
                print("将文件{}命名为{}失败".format(file_path, new_name))
            else:
                print("将文件{}命名为{}成功".format(file_path, new_name))


def rename_live_photo_in_dir(target_dir: str):
    """
    给Live Phone重命名
    :param target_dir: 目标文件夹
    :return: None
    """
    for entry in os.scandir(target_dir):
        heic_file_name = entry.name
        heic_file_path = entry.path
        if heic_file_name.startswith("."):
            # 系统隐藏文件/文件夹不处理
            continue
        if os.path.isdir(heic_file_path):
            rename_live_photo_in_dir(heic_file_path)

        suffix = get_file_suffix(heic_file_name)
        if suffix is None:
            # 无后缀名的文件不处理
            print("{}无后缀名不进行处理 ".format(heic_file_path))
            continue
        if len(suffix.strip()) == 0:
            continue

        if suffix != ".heic":
            continue
        dir_path = os.path.split(heic_file_path)[0]
        mov_file_path = os.path.splitext(heic_file_path)[0] + ".mov"
        if not os.path.exists(mov_file_path):
            # mov 文件不存在就不是一个标准的Live Photo
            continue

        new_name = gen_name_for_video(mov_file_path)
        rename_file(heic_file_path, os.path.join(dir_path, new_name + ".heic"))
        rename_file(mov_file_path, os.path.join(dir_path, new_name + ".mov"))


def rename_file(old_name, new_name) -> bool:
    """
    重命名文件
    :param old_name: Old name for the file.
    :param new_name: New name for the file.
    :return: True 成功
    """
    if old_name is None or new_name is None:
        return False
    try:
        os.rename(old_name, new_name)
        return True
    except NotImplementedError or OSError:
        return False


def gen_name_for_img(img_path: str) -> str:
    """
    提取图片文件的exif信息生成新文件名称
    :param img_path: 图片文件的全路径名称
    :return: 新名称
    """
    img = open(img_path, "rb")
    tags = exifread.process_file(img)
    now = datetime.datetime.now()
    shot_time = tags.get('EXIF DateTimeOriginal', now)
    holder_label = "@"
    make = tags.get('Image Make')
    if make is not None:
        make = make.values.strip()
    else:
        make = holder_label
    model = tags.get('Image Model')
    if model is not None:
        model = model.values.strip()
    else:
        model = holder_label
    return "{}_{}_{}".format(shot_time, make, model).replace(" ", "_")


def gen_name_for_video(video_path: str):
    """
    提取视频时长放在名称上
    :param video_path:
    :return:
    """
    file_create_time = os.path.getctime(video_path)
    time_str = datetime.datetime.fromtimestamp(file_create_time)
    clip = VideoFileClip(video_path)
    duration = format_duration(clip.duration)
    new_name = "{}_{}".format(time_str, duration).replace(" ", "_")
    return new_name


def fix_video_file_name(video_full_name: str):
    """
    修复视频文件名称上
    :param video_full_name:
    :return:
    """
    p_n = os.path.split(video_full_name)
    if len(p_n) < 2:
        return None
    v_name = p_n[1]
    name_parts = v_name.split(".")
    if len(name_parts) < 1:
        return None
    elif len(name_parts) > 2:
        suffix = name_parts[1][0:3]
    else:
        suffix = name_parts[1]
    new_name = "{}.{}".format(name_parts[0], suffix)
    return new_name


def format_duration(video_duration: int) -> str:
    """
    格式化时间
    :param video_duration:
    :return:
    """
    M, H = 60, 60 ** 2
    if video_duration < M:
        return u'%ds' % int(video_duration)
    else:
        if video_duration < H:
            minute = int(video_duration / M)
            second = int(video_duration % M)
            return u'%dm%ds' % (minute, second)
        else:
            hour = int(video_duration / H)
            minute = int(video_duration % H / M)
            second = int(video_duration % H % M)
        return u'%dh%dm%ds' % (hour, minute, second)


if __name__ == "__main__":
    print("作为模块倒入的时候不执行！")
    # clutter_path = input("输入文件名：")
    # rename_file_in_dir(clutter_path)
    test_dir = "/Volumes/SSD256/整理后˚的照片/写真照片/live_photo"
    # rename_all_files_in_dir(test_dir)
    rename_live_photo_in_dir(test_dir)

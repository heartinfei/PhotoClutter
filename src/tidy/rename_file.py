#!/usr/bin/python3
# -*- coding: utf-8 -*-

import exifread
import os
import datetime
from moviepy.editor import VideoFileClip

# 图片格式
img_types = ('.jpg', '.jpeg', '.png', '.heic', '.dng')

# 视频格式
video_types = ('.mp4', '.mpeg4', '.mov', '.3gp')


def rename_file(old_name, new_name) -> bool:
    """
    重命名文件
    :param old_name: Old name for the file.
    :param new_name: New name for the file.
    :return: True 成功
    """
    try:
        os.rename(old_name, new_name)
        return True
    except NotImplementedError or OSError:
        return False


def rename_files_in_dir(target_dir):
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
            rename_files_in_dir(file_path)
            continue
        else:
            try:
                suffix = os.path.splitext(file_name)[1]
            except IndexError:
                # 无后缀名的文件不处理
                print("{}无后缀名不进行处理 ".format(file_path))
                continue
            if len(suffix.strip()) == 0:
                continue
            if suffix in img_types:
                # 对照片重命名
                new_name = gen_name_for_img(file_path) + suffix
                new_file_path = os.path.join(target_dir, new_name)
                if not rename_file(file_path, new_file_path):
                    print("将文件{}命名为{}失败".format(file_path, new_name))
            elif suffix in video_types:
                # 对视频文件重命名
                new_name = os.path.join(target_dir, gen_name_for_video(file_path))
                rename_file(file_path, new_name)


def gen_name_for_img(img_full_name: str) -> str:
    img = open(img_full_name, "rb")
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


def gen_name_for_video(video_full_name: str) -> str:
    clip = VideoFileClip(video_full_name)
    duration = format_duration(clip.duration)
    return u'%s%s.mp4' % (clip.filename, duration)


def format_duration(video_duration: int) -> str:
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
    rename_files_in_dir("/Users/smzdm/Public/ImgSource")

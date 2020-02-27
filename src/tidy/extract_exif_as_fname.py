#!/usr/bin/python3
# -*- coding: utf-8 -*-

import exifread
import os
import datetime
from moviepy.editor import VideoFileClip


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
            if element.endswith(".jpeg"):
                # 对照片重命名
                new_name = os.path.join(d, gen_name_for_img(f_name))
                rename_file(f_name, new_name)
            elif element.endswith(".mp4") or element.endswith(".mov"):
                # 对视频文件重命名
                new_name = os.path.join(d, gen_name_for_video(f_name))
                rename_file(f_name, new_name)


def rename_file(old_name, new_name):
    """
    重命名文件
    :param old_name:
    :param new_name:
    :return:
    """
    try:
        os.rename(old_name, new_name)
    except NotImplementedError:
        print("extract_exif_as_fname-->NotImplementedError")


def gen_name_for_img(img_full_name: str) -> str:
    img = open(img_full_name, "rb")
    tags = exifread.process_file(img)
    now = datetime.datetime.now()
    shot_time = tags.get('EXIF DateTimeOriginal', now)
    make = tags.get('Image Make', "unknow")
    model = tags.get('Image Model', 'unknow')
    return "{}_{}_{}.jpeg".format(shot_time, make, model).replace(" ", "_")


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
    clutter_path = input("输入批处理文件名：")
    rename_file_in_dir(clutter_path)

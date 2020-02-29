import os

# 图片格式
img_types = ('.jpg', '.jpeg', '.png', '.dng')
# 视频格式
video_types = ('.mp4', '.mpeg', '.mov', '.3gp')
# video_types = ()


def get_file_suffix(file_name):
    try:
        return os.path.splitext(file_name)[1]
    except IndexError:
        return None

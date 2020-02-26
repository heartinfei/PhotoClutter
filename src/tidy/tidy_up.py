import os
import shutil


def empty_target(log_file: str):
    log = open(log_file, "r")
    for line in log.readline():
        try:
            os.remove(line)
        except NotImplementedError:
            print("tidy_up-->NotImplementedError")


def del_by_list(file_list: list):
    for path in file_list:
        try:
            os.remove(path)
        except NotImplementedError:
            print("tidy_up-->NotImplementedError")


def move_to_target_dir(src: str, dst: str):
    for element in os.listdir(str):
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
    batch_file_name = input("输入批处理文件名：")
    empty_target(batch_file_name)

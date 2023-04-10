#!/usr/bin/python3
from pydub import AudioSegment
from os import walk, remove, rename
from moviepy.editor import *
import re


# 把文件里的(P1. 1).mp3改成001.mp3
def change_name(file_name):
    f_name = file_name
    f_name = re.sub(r".\(P(\d)\. (\d)\)", lambda m: m.group(1).zfill(3), f_name)
    rename(file_name, f_name)
    return f_name


def get_files(ex="mp3"):
    af = []
    for (p, d, f) in walk("./"):
        for s in f:
            if s[-3:] == ex:
                n = change_name(s)
                af.append(n)
    af.sort()
    return af


def mp4_mp3(file):
    file_name = file[:-4]
    c = AudioFileClip(file)
    c.write_audiofile(f"{file_name}.mp3", bitrate="50k")
    c.close()

# 要把几个文件合并成一个


def ask_step():
    step = input("How many files merge to 1: ")
    try:
        step = int(step)
    except:
        print("input must be number")
        step = ask_step()
    return step

# 把几个文件合并成一个


def merge_mp3(files, new_name):
    sound = None
    for f in files:
        print(f"# load {f}...")
        if not sound:
            sound = AudioSegment.from_mp3(f)
        else:
            sound = sound.append(AudioSegment.from_mp3(f))
        remove(f)
    print(f"# ==> export to {new_name}.mp3")
    sound.export(f"{new_name}.mp3", format="mp3")

def main():
    print("#"*60)
    # loop所有mp4文件
    fmp4 = get_files("mp4")
    for f in fmp4:
        print(f)
        # mp4转mp3
        mp4_mp3(f)
        # 删掉原mp4
        remove(f)
    # loop 所有mp3文件
    fmp3 = get_files("mp3")
    if len(fmp3) == 1:
        print("Only 1 file, finished!")
        exit()
    print(f"# All {len(mp3)} files find!")
    # 获得扩展名和序号前的名字
    fin_name = fmp3[0][:-7]
    step = ask_step()
    # 每次mp3文件array的开始和结束index
    st = 0
    to = 0
    new_count = 1
    while(to < len(fmp3)):
        to = st+step
        print(st, to)
        merge_mp3(fmp3[st:to], f"{fin_name}_{new_count:03d}")
        # 取后面的文件
        new_count += 1
        st = to


if __name__ == "__main__":
    main()

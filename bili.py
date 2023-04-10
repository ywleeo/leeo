#!/usr/bin/python3
import subprocess
import json
import you_get
import re


def video_json(url: str):
    cmd = f"you-get --json {url}"
    return json.loads(subprocess.check_output(cmd, shell=True))


def download_video(url: str, title: str, is_playlist="--playlist"):
    cmd = f"you-get {is_playlist} --no-caption --format={title} {url}"
    subprocess.run(cmd, shell=True)


def get_formats(vinfo):
    formats = []
    idx = 0
    for k, v in vinfo["streams"].items():
        formats.append(k)
        print("-" * 60)
        print(idx, ".", k, ",", round(
            v["size"] / (1024 * 1024), 2), "M", ",", v["container"], v["quality"])
        idx += 1
    print("-" * 60)
    return formats

def main():
    print("#" * 60)
    url = input("# Bilibili URL: ")
    if url == "":
        exit()
    vinfo = video_json(url)
    # 判断是否是playlist
    utitle = re.findall(r".\(P\d\. \d+\.mp4\)",vinfo["title"])
    fms = get_formats(vinfo)
    fm = input("@ Choose formats: ")
    fm_choose = fms[int(fm)]
    print(f"# <{fm_choose}> is choosed! ")
    # 是playlist
    if len(utitle)>0:
        is_playlist = input("@ down playlist? y/n ")
        if is_playlist == "y":
            download_video(url, fm_choose)
        else:
            download_video(url, fm_choose, "")
    download_video(url, fm_choose, "")
    exit()

if __name__ == "__main__":
    main()

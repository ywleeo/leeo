import subprocess
import json


def video_json(url: str):
    cmd = f"you-get --json {url}"
    return json.loads(subprocess.check_output(cmd, shell=True))


def download_video(url: str, title: str):
    cmd = f"you-get --playlist --format={title} {url}"
    subprocess.run(cmd, shell=True)


def get_min(url):
    title = ""
    min_size = None
    for k, v in video_json(url)["streams"].items():
        if not min_size:
            min_size = v["size"]
        elif min_size > v["size"]:
            min_size = v["size"]
            title = k

        print("#" * 60)
        print(k)
        print(round(v["size"] / (1024 * 1024), 2), "M")
        print(v["container"], v["quality"])
    return title


if __name__ == "__main__":
    print("=" * 100)
    while True:
        url = input("Bilibili url: ")
        if url == "":
            exit()
        title = get_min(url)
        download_video(url, title)
        exit()

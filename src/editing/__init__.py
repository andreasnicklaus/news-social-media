from . import moviepy_edit as mpy
from .sources import filepath_from_url
from datetime import datetime as dt


def download_videos(video_urls):
    clips = []
    for i, video_url in enumerate(video_urls):
        if video_url.startswith("http"):
            print(f"loading footage ({i}/{len(video_urls)})...")
            file_path = filepath_from_url(video_url)
        else:
            file_path = video_url

        clips.append(file_path)
    return clips


def create_video(video_urls, audio, title, abstract):
    now = dt.now()
    out_path = (
        f"out/{now.strftime('%Y')}-{now.strftime('%m')}-{now.strftime('%d')}.post.mp4"
    )
    file_paths = download_videos(video_urls)
    return mpy.create_video(out_path, file_paths, audio, title, abstract)

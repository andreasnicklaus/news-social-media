# Import everything needed to edit video clips
# from moviepy.editor import *
from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    ImageClip,
    CompositeVideoClip,
)
from .sources import filepath_from_url
from datetime import datetime as dt


def create_video(video_urls, audio, title, abstract):
    audioclip = AudioFileClip(audio)

    clips = []
    for i, video_url in enumerate(video_urls):
        if video_url.startswith("http"):
            print(f"loading footage ({i}/{len(video_urls)})...")
            file_path = filepath_from_url(video_url)
        else:
            file_path = video_url
        clips.append(
            VideoFileClip(file_path).subclip(0, audioclip.duration / len(video_urls))
        )

    video = concatenate_videoclips(clips).set_audio(audioclip)

    w, h = video.size

    print(w, h)
    print(audio, title, abstract)

    titleclip = (
        TextClip(
            title,
            font="AvantGarde-Demi",
            color="white",
            kerning=5,
            fontsize=100,
            size=(w * 0.8, h * 0.8),
            method="caption",
        )
        .set_duration(3)
        .on_color(color=[10, 10, 10], col_opacity=0.8)
        .set_position((w * 0.1, h * 0.1))
    )

    abstractclip = (
        TextClip(
            abstract,
            font="AvantGarde-Demi",
            color="white",
            kerning=3,
            fontsize=60,
            size=(w * 0.8, None),
            method="caption",
        )
        .set_duration(video.duration - 3)
        .on_color(color=[10, 10, 10], col_opacity=0.8)
        .set_position((w * 0.1, h * 0.1))
        .set_start(3)
    )

    brandingClip = (
        ImageClip("src/branding/poweredby_nytimes_150c.png")
        .set_position((w * 0.1, h * 0.9))
        .set_duration(video.duration)
        .resize(width=(0.4 * w))
    )

    video = CompositeVideoClip([video, titleclip, abstractclip, brandingClip])

    now = dt.now()
    file_name = (
        f"out/{now.strftime('%Y')}-{now.strftime('%m')}-{now.strftime('%d')}.post.mp4"
    )

    video.write_videofile(file_name, logger=None)

    return file_name

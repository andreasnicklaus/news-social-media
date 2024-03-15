from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    concatenate_videoclips,
    TextClip,
    ImageClip,
    CompositeVideoClip,
)

from PIL import Image

Image.ANTIALIAS = Image.LANCZOS


def create_video(out_path, file_paths, audio, title, abstract):
    audioclip = AudioFileClip(audio)

    clips = []
    for i, file_path in enumerate(file_paths):
        clips.append(
            VideoFileClip(file_path).subclip(0, audioclip.duration / len(file_paths))
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

    video.write_videofile(out_path, audio_codec="aac", audio_bitrate="64k")

    return out_path

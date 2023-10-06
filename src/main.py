from news import get_all, get_one
from footage import get_photos_by_keyword, get_videos_by_keyword
from editing import create_video
from tts import tts
from socials import post
from mail import send
import os


def clear_directory(dir):
    for f in os.listdir(dir):
        filepath = f"{dir}/{f.split('/')[-1].split('?')[0]}"
        try:
            os.remove(filepath)
        except Exception:
            print(f"{filepath} not found")


def get_video_links_from_keywords(keywords, n):
    videos = [get_videos_by_keyword(kw, n // len(keywords) + 1) for kw in keywords]

    footage = [
        video_object.get("video_files")
        for video_object in videos
        if video_object is not None
    ][:n]

    vid_files = []
    for v_files in footage:
        for v_file in v_files:
            if v_file.get("quality") == "hd" and v_file.get("width") == 1080:
                vid_files.append(v_file.get("link"))

    return vid_files


def start():
    story = get_one()

    title = story.get("title")
    abstract = story.get("abstract")
    audio_text = f"{title}. {abstract}"
    word_count = len(audio_text.split(" "))
    audio_path = tts(text=audio_text)
    # print(audio_text)
    assert title is not None, "Title must exist."
    assert abstract is not None, "Abstract must exist."
    assert audio_text is not None, "Audiotext must exist."
    assert word_count is not None, "word_count must exist."
    assert audio_path is not None, "audio_path must exist."

    keywords = story.get("adx_keywords").split(";")
    assert len(keywords) > 0, f"Die Story enthält keine Keywords."

    vid_files = get_video_links_from_keywords(keywords, n=word_count // 5)

    assert (
        len(vid_files) > 0
    ), f"Für die Keywords: [{', '.join(keywords)}] wurde kein Video gefunden."

    video_path = create_video(vid_files, audio_path, title, abstract)

    clear_directory("sources")

    caption = f"""{title}
    {abstract}

    #Follow for more #news everyday!

    {' '.join([f'#{kw.split("(")[0].replace(" ", "").replace(",", "")}' for kw in filter(lambda kw: not kw.startswith("Content") and not kw.startswith("internal"), keywords)])}
        
    Data provided by The New York Times (https://developer.nytimes.com)"""

    print(caption)
    send(caption, video_path)
    # TODO: integrate social media
    post(video_path, caption)

    # clear_directory("out")


if __name__ == "__main__":
    start()

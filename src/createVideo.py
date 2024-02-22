import os
from footage import get_videos_by_keyword
from editing import create_video
from mail import send
from socials import post
import yaml

def clear_directory(dir):
    for f in os.listdir(dir):
        filepath = f"{dir}/{f.split('/')[-1].split('?')[0]}"
        try:
            os.remove(filepath)
        except Exception:
            print(f"{filepath} not found")

def get_video_links_from_keywords(keywords, n):
    footage = [
        f.get("video_files")
        for kw in keywords
        for f in get_videos_by_keyword(kw, n // len(keywords) + 1)
    ][:n]

    vid_files = []
    for v_files in footage:
        for v_file in v_files:
            if v_file.get("quality") == "hd" and v_file.get("width") == 1080:
                vid_files.append(v_file.get("link"))

    return vid_files

audio_path = "out/tts.wav"

def start():
    with open("out/audio_text.txt", "r") as audio_text_file:
        audio_text = audio_text_file.read()
    word_count = len(audio_text.split(" "))

    with open("out/story.yaml", "r") as story_file:
        story = yaml.safe_load(story_file)
    title = story.get("title")
    abstract = story.get("abstract")
    keywords = story.get("adx_keywords").split(";")
    assert len(keywords) > 0, f"Die Story enthält keine Keywords."
    assert title is not None, "Title must exist."
    assert abstract is not None, "Abstract must exist."
    assert audio_text is not None, "Audiotext must exist."
    assert word_count is not None, "word_count must exist."

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
    post(video_path, caption)

    clear_directory("out")


if __name__ == "__main__":
    start()
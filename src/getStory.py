from news import get_all, get_one
import yaml
import os

def start():
    story = get_one()

    title = story.get("title")
    abstract = story.get("abstract")
    audio_text = f"{title}. {abstract}"
    # print(audio_text)
    assert title is not None, "Title must exist."
    assert abstract is not None, "Abstract must exist."
    assert audio_text is not None, "Audiotext must exist."

    with open("./out/audio_text.txt", "w") as audio_text_file:
      audio_text_file.write(audio_text)
      print(os.path.realpath(audio_text_file.name))
    with open("./out/story.yaml", "w") as story_file:
      yaml.dump(story, story_file, sort_keys=False)
      print(os.path.realpath(story_file.name))

    print(os.listdir("/usr/src/app/out"))

if __name__ == "__main__":
  start()
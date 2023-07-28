from . import pexels

def get_photos_by_keyword(keyword, n=1):
    return pexels.get_photos_by_keyword(keyword, n)

def get_videos_by_keyword(keyword, n=1):
    return pexels.get_videos_by_keyword(keyword, n)
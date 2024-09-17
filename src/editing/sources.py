import requests


def filepath_from_url(url):
    file_name = "sources/" + url.split("/")[-1].split("?")[0]

    # create response object
    r = requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"})

    # download started
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return file_name

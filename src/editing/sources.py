import requests


def filepath_from_url(url):
    file_name = "sources/" + url.split("/")[-1].split("?")[0]

    # create response object
    r = requests.get(url, stream=True)

    # download started
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

    return file_name

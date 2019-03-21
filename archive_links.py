import json
import sys
import urllib.request

from urlextract import URLExtract


def find_urls_in_text(text):
    extractor = URLExtract()
    return extractor.find_urls(text)

def get_final_redirected_url(url):
    try:
        response = urllib.request.urlopen(url)
        return response.geturl()
    except urllib.error.HTTPError as e:
        print(f"Could not access {url} {e}")
        return None

def archive_url_to_waybackmachine(url):
    root_url = "https://web.archive.org/save/"
    url = get_final_redirected_url(url)
    if url:
        try:
            urllib.request.urlopen(root_url + url)
            return retrieve_archived_url_from_waybackmachine(url)
        except urllib.error.HTTPError as e:
            print(f"Could not access {url} {e}")
            return None

def retrieve_archived_url_from_waybackmachine(url):
    url = get_final_redirected_url(url)
    if url:
        try:
            response = urllib.request.urlopen(
                f'http://archive.org/wayback/available?url={url}')
            data = json.loads(response.read())
            return data.get("archived_snapshots").get("closest").get("url")
        except urllib.error.HTTPError as e:
            print(f"Could not access {url} {e}")



if __name__ == "__main__":

    assert len(sys.argv) == 2, "Please specify a text file as input argument!"

    with open(sys.argv[1], "r") as f:
        data = f.read()

    for url in set(find_urls_in_text(data)):

        url = url.strip(r"()[]{}")

        # check if already archived:
        archived_url = retrieve_archived_url_from_waybackmachine(url)

        if not archived_url:
            # archive!
            archived_url = archive_url_to_waybackmachine(url)

        if archived_url:
            print(archived_url)
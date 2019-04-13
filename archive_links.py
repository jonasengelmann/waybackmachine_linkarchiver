import argparse
import json
import logging
import urllib.request

from urlextract import URLExtract


def clean_url(url):
    url = url.strip(r'()[]{}')
    url = url.replace("ftp://", "http://")
    if not url.lower().startswith('http'):
        url = f'http://{url}'
    return url


def find_urls_in_text(text):
    extractor = URLExtract()
    return set(extractor.find_urls(text))


def get_final_redirected_url(url):
    try:
        response = urllib.request.urlopen(url)
        return response.geturl()
    except (urllib.error.HTTPError, urllib.error.URLError) as ex:
        logging.error(f'Could not access {url} {ex}')
        return None


def push_url_to_waybackmachine(url):
    root_url = 'https://web.archive.org/save/'
    url = get_final_redirected_url(url)
    if url:
        try:
            urllib.request.urlopen(root_url + url)
            return fetch_archived_url_from_waybackmachine(url)
        except (urllib.error.HTTPError, urllib.error.URLError) as ex:
            logging.error(f'Could not archive {url} {ex}')
            return None


def fetch_archived_url_from_waybackmachine(url):
    url = get_final_redirected_url(url)
    if url:
        try:
            response = urllib.request.urlopen(
                f'http://archive.org/wayback/available?url={url}')
            data = json.loads(response.read())
            return data.get('archived_snapshots').get('closest').get('url')
        except (urllib.error.HTTPError, urllib.error.URLError) as ex:
            logging.error(f'Could not access {url} {ex}')
            return None


def archive_url(url, force_new_archive=False):
    archived_url = None

    if not force_new_archive:
        # check if url already archived
        archived_url = fetch_archived_url_from_waybackmachine(url)

    if not archived_url:
        archived_url = push_url_to_waybackmachine(url)

    if archived_url:
        logging.info(archived_url)
        return archived_url


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', type=str,
                       help='URL you want to archive')
    group.add_argument('-f', '--file', type=str,
                       help='''Path to a text file containing urls. The
                               script will make a copy of the text file and
                               replace all urls with their archived version.
                               The text file can also contain non url
                               content''')
    parser.add_argument('--force', action='store_true',
                        help='''When an url is already archived, we can
                                use this argument to assure that a new
                                archived version is created''')

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s%(message)s')

    logging.info('Archiving urls...')

    if args.url:
        url = clean_url(args.url)
        archive_url(url, args.force)

    if args.file:
        data = open(args.file, 'r').read()

        with open(args.file + "_urls_archived", 'w') as out_file:
            for url in find_urls_in_text(data):
                new_url = archive_url(clean_url(url), args.force)
                if new_url:
                    data = data.replace(url, new_url)
            out_file.write(data)

    logging.info("Done!")

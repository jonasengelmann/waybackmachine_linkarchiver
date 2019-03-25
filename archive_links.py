import argparse
import json
import logging
import sys
import urllib.request

from urlextract import URLExtract


def clean_url(url):
    url = url.strip(r'()[]{}')
    if not url.lower().startswith(('http','ftp://')):
        url = f'http://{url}'
    return url

def find_urls_in_text(text):
    extractor = URLExtract()
    return set(extractor.find_urls(text))

def get_final_redirected_url(url):
    try:
        response = urllib.request.urlopen(url)
        return response.geturl()
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        logging.error(f'Could not access {url} {e}')
        return None

def push_url_to_waybackmachine(url):
    root_url = 'https://web.archive.org/save/'
    url = get_final_redirected_url(url)
    if url:
        try:
            urllib.request.urlopen(root_url + url)
            return fetch_archived_url_from_waybackmachine(url)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logging.error(f'Could not archive {url} {e}')
            return None

def fetch_archived_url_from_waybackmachine(url):
    url = get_final_redirected_url(url)
    if url:
        try:
            response = urllib.request.urlopen(
                f'http://archive.org/wayback/available?url={url}')
            data = json.loads(response.read())
            return data.get('archived_snapshots').get('closest').get('url')
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logging.error(f'Could not access {url} {e}')
            return None

def archive_url(url, force_new_archive=False):
    archived_url = None

    if not force_new_archive:
        # check if url already archived
        archived_url = fetch_archived_url_from_waybackmachine(url)

    if not archive_url:
        archived_url = push_url_to_waybackmachine(url)

    if archived_url:
        logging.info(archived_url)
        return archived_url


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='URL you want to archive.', type=str)
    parser.add_argument('-t','--textfile',
                        help='''Path to a textfile containing urls. The script 
                                will make a copy of the textfile and replace all
                                urls with their archived version. The textfile 
                                can also contain non url content.''', type=str)
    parser.add_argument('-f', '--force',
                        help = '''When an an url is already archived, we can
                                  use this parameter to assure a new archived
                                  version is created.''',
                        action = 'store_true')


    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s%(message)s')

    if not args.url and not args.textfile:
        logging.error('Please specify an url or a textfile with containing urls!')
        sys.exit(1)
    
    logging.info('Archiving links...')

    if args.url:
        url = clean_url(args.url)
        archive_url(url, args.force)
        
    if args.textfile:
        with open(args.textfile, 'r') as in_file:
            data = in_file.read()
        
        with open(args.textfile + "_urls_archived", 'w') as out_file:
            for url in find_urls_in_text(data):
                new_url = archive_url(clean_url(url), args.force)
                if new_url:
                    data = data.replace(url, new_url)
            out_file.write(data)
    
    logging.info("Done!")
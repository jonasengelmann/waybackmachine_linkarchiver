# waybackmachine linkarchiver
Easily make waybackmachine archive your links and replace them with their archived version in your documents.

This script will find all links in a specified document, save them to the waybackmachine and return the archived urls. Replace them in your document, such as .tex or .bib and never have to deal with dead links again. 


### Prerequisites

```
pip install -r requirements.txt
```

### Usage

```
usage: archive_links.py [-h] (-u URL | -f FILE) [--force]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL you want to archive
  -f FILE, --file FILE  Path to a text file containing urls. The script will
                        make a copy of the text file and replace all urls with
                        their archived version. The text file can also contain
                        non url content
  --force               When an url is already archived, we can use this
                        argument to ensure that a new archived version is
                        created
```

### Example usage


```
python archive_links.py --file example_document_containing_links.txt --force
python archive_links.py --url www.wikipedia.org
```

For now, only files are supported that can be read as simple text. PDF and DOCX support will be added soon!

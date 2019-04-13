# waybackmachine linkarchiver
Easily make waybackmachine archive your links and replace them with their archived version in your documents.

This script will find all links in a specified document, save them to the waybackmachine and return the archived urls. Replace them in your document, such as .tex or .bib and never have to deal with dead links agian. 


### Prerequisites

```
pip install -r requirements.txt
```

### Usage

```
archive_links.py [-h] (-u URL | -f FILE) [--force]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL you want to archive.
  -f FILE, --file FILE  Path to a textfile containing urls. The script will
                        make a copy of the textfile and replace all urls with
                        their archived version. The textfile can also contain
                        non url content.
  --force               When an an url is already archived, we can use this
                        parameter to assure a new archived version is created.
```

### Example usage


```
python archive_links.py --file example_document_containing_links.txt --force
python archive_links.py --url www.wikipedia.org
```

For now, only files are supported that can be read as simple text. PDF and DOCX support will be added soon!

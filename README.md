# waybackmachine linkarchiver
Easily make waybackmachine archive your links and replace them with their archived version in your documents.

This script will find all links in a specified document, save them to the waybackmachine and return the archived urls. Replace them in your document, such as .tex or .bib and never have to deal with dead links agian. 


### Prerequisites

```
pip install -r requirements.txt
```

### Example usage


```
python archive_links.py -t example_document_containing_links.txt
python archive_links.py -u www.wikipedia.org
```

For now, only files are supported that can be read as simple text. PDF and DOCX support will be added soon!

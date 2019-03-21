# waybackmachine linkarchiver
Easily make waybackmachine archive your links and replace them with their archived version in your documents.

This script will find all links in a specified document, save them to the waybackmachine and return the archived urls. Replace them in your document, such as .tex or .bib and never have to deal with dead links agian. 


### Prerequisites

```
pip install -r requirements.txt
```

### Example usage


```
python archive_links.py example_document_containing_links.txt
```

For now, only files that can be read as simple text are supported. PDF and DOCX support will be added soon!

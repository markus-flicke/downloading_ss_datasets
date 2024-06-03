# 2020 [S2ORC](https://allenai.org/data/s2orc) dataset
Published by Kyle Lo, Lucy Lu Wang, Mark Neumann, Rodney Kinney, Daniel S. Weld at Semantic Scholar.  
This readme is dated 03.06.2024.  

### Download this dataset
1. Run `main.download_ss_dataset("s2orc")`, code taken from 
2. Unzip all the downloaded files. For me, Ubuntu's `unzip` didn't work and I used the file explorer's `extract here` option.
3. The extracted files are in JSON format and I was able to read them using Python's json.load().


### Dataset structure
JSON files with one paper per line. Each paper has the following fields:
- `corpusid`: Not sure what it is
- `externalids`: External IDs of the paper
    - `arxiv`: ArXiv ID
    - `mag`: Microsoft Academic Graph ID
    - `acl`: ACL ID
    - `pubmed`: PubMed ID
    - `pubmedcentral`: PubMed Central ID
    - `dblp`: DBLP ID
    - `doi`: DOI
- `content`:
    - `source`: 
        - `pdfurls`: URL(s) to the PDF
        - `pdfsha`: SS SHA key to the PDF
        - `oainfo`:
    - `text`: Full text of the paper
    - `annotations`: Annotations are always of shape [{"start": a, "end": b}, ...] with `a` and `b` being a natural number. They are character indices of the annotation in the text. The following annotations are available:
        - `abstract`: 
        - `author`: 
        - `authoraffiliation`: 
        - `authorfirstname`: 
        - `authorlastname`: 
        - `bibauthor`: 
        - `bibauthorfirstname`: 
        - `bibauthorlastname`: 
        - `bibentry`: 
        - `bibref`: 
        - `bibtitle`: 
        - `bibvenue`: 
        - `figure`: 
        - `figurecaption`: 
        - `figureref`: 
        - `formula`: 
        - `paragraph`: 
        - `publisher`: 
        - `sectionheader`: 
        - `table`: 
        - `tableref`: 
        - `title`: 
        - `venue`: 

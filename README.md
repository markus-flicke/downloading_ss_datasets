# Semantic Scholar Datasets
This readme is dated 03.06.2024.  

## Download a dataset
1. Run `download_dataset.download_dataset("s2orc")`
    - Available datasets: `s2orc`, `abstracts`, `authors`, `citations`, `embeddings-specter_v1`, `embeddings-specter_v2`, `paper-ids`, `papers`, `publication-venues`, `tldrs`
    - [S2AG](https://dl.acm.org/doi/fullHtml/10.1145/3487553.3527147) has 205M publications, 121M authors and 2.5B citation edges. 
2. Unzip all the downloaded files. For me, Ubuntu's `unzip` didn't work and I used the file explorer's `extract here` option.
3. The extracted files are in JSON format and I was able to read them using Python's json.load().

## Update a dataset
https://api.semanticscholar.org/api-docs/datasets#tag/Incremental-Updates

## Papers
- `corpusid`:
- `externalids`: example: {'ACL': None, 'DBLP': None, 'ArXiv': None, 'MAG': '609515471', 'CorpusId': '211932277', 'PubMed': None, 'DOI': None, 'PubMedCentral': None}
- `url`: semantic scholar url
- `title`:
- `authors`: example: [{'authorId': '77672491', 'name': '加藤 智美'}, {'authorId': '52238866', 'name': '鈴木 康之'}]
- `venue`:
- `publicationvenueid`:
- `year`:
- `referencecount`:
- `citationcount`:
- `influentialcitationcount`:
- `isopenaccess`:
- `s2fieldsofstudy`:
- `publicationtypes`:
- `publicationdate`:
- `journal`:

## Authors
- `authorid`: SS author ID
- `externalids`: example: {'DBLP': ['Dongsheng Wu'], 'ORCID': None}
- `url`: URL to the author's Semantic Scholar page
- `name`: 
- `aliases`: Aliases of the author
- `affiliations`: 
- `homepage`: 
- `papercount`: 
- `citationcount`: 
- `hindex`: 

## 2020 [S2ORC](https://allenai.org/data/s2orc)
Published by Kyle Lo, Lucy Lu Wang, Mark Neumann, Rodney Kinney, Daniel S. Weld at Semantic Scholar.  


### Dataset structure
JSON files with one paper per line. Each paper has the following fields:
- `corpusid`: Not sure what it is
- `externalids`: 
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

## Citations
Not all zip files (4,8,14) extracted successfully. Many zip files also extracted into multiple parts. Not sure why
- `citationid`:
- `citingcorpusid`: 
- `citedcorpusid`: 
- `isinfluential`:
- `contexts`: Contexts in which the citation is made
- `intents`: example: [['methodology']]


# PostgreSQL faster search
Use indexes on columns that we search in
## BigInt search
`CREATE INDEX ON paper_authors (author_id);`
`CREATE INDEX ON paper_authors (corpus_id);`
## Text search
I would like this kind of query to run in under 1sec:  
`select name, h_index from authors where name like '%Geiger%';`  
The above query takes 1.9sec on my machine  
### GIN search
`CREATE INDEX name_index_gist on authors USING GIST (to_tsvector('english', name));`
```
ss_bootstrapping=# select author_id, name, h_index, paper_count, citation_count from authors where to_tsvector('english', name) @@ to_tsquery('english', 'Geiger') order by h_index desc limit 10;;
 author_id |      name      | h_index | paper_count | citation_count 
-----------+----------------+---------+-------------+----------------
   2727510 | B. Geiger      |     109 |         413 |          52896
  47237027 | Andreas Geiger |      78 |         187 |          49182
  50370265 | H. Geiger      |      51 |         263 |          10596
 145674565 | J. Geiger      |      50 |         223 |          10070
  74667191 | A. Geiger      |      49 |         154 |           8295
  33859605 | T. Geiger      |      47 |         139 |          14318
 144527211 | D. Geiger      |      47 |         123 |          15638
  32844974 | H. H. Geiger   |      46 |         203 |           7476
   4121084 | F. Geiger      |      42 |         239 |           6144
   1951720 | D. Geiger      |      40 |         111 |           4215
(10 rows)

Time: 45,304 ms
Time: 0,029 ms
```
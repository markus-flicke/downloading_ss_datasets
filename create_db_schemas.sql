CREATE DATABASE ss_bootstrapping;

CREATE TABLE papers (
    corpus_id INT PRIMARY KEY,
    title TEXT NOT NULL,
    abstract TEXT,
    publication_date DATE,
    url TEXT,
    journal TEXT,
    venue TEXT,
    year INT,
    citation_count INT,
    authors text[]
);

CREATE TABLE authors (
    author_id BIGINT PRIMARY KEY,
    name TEXT NOT NULL, 
    paper_count INT,
    citation_count INT,
    h_index INT
);

CREATE TABLE paper_authors (
    corpus_id INT NOT NULL,
    author_id BIGINT NOT NULL,
    PRIMARY KEY (corpus_id, author_id),
    FOREIGN KEY (corpus_id) REFERENCES papers(corpus_id)
);

ALTER TABLE papers DROP COLUMN citation_count;
ALTER TABLE papers ADD citation_count INT;
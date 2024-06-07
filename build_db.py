import os
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm

HARDDRIVE_PATH = '/media/scholar/cca30a4f-fb5b-4ec5-9bca-8f51dad1364c/'

def append_df_to_sql(df, table_name):
    engine = create_engine('postgresql://scholar:scholar@localhost/ss_bootstrapping')
    df.to_sql(table_name, engine, if_exists='append', index=False)

def build_authors():
    for filename in tqdm(os.listdir(os.path.join(HARDDRIVE_PATH, 'authors'))):
        filepath = os.path.join(HARDDRIVE_PATH, 'authors', filename)
        if filename.endswith('.zip'):
            continue

        df = pd.read_json(filepath, lines=True)
        df = df.rename(columns={'authorid': 'author_id',
                                'papercount': 'paper_count',
                                'citationcount': 'citation_count',
                                'hindex': 'h_index',
                                })
        df = df[['author_id', 'name', 'paper_count', 'citation_count', 'h_index']]
        df = df.dropna(axis = 0, subset=['author_id', 'name'])
        append_df_to_sql(df, 'authors')


def build_papers():
    for filename in tqdm(os.listdir(os.path.join(HARDDRIVE_PATH, 'papers', 'shards'))):
        filepath = os.path.join(HARDDRIVE_PATH, 'papers', 'shards', filename)
        if filename.endswith('.zip'):
            continue

        full_papers_df = pd.read_json(filepath, lines=True)
        df = full_papers_df.rename(columns={'corpusid': 'corpus_id',
                            'publicationdate': 'publication_date',
                            'citationcount': 'citation_count',
                            'hindex': 'h_index',
                            })
        df = df[['corpus_id', 'title', 'publication_date', 'url', 'journal', 'venue', 'year']]
        df['abstract'] = None
        df['journal'] = df['journal'].apply(lambda x: x['name'] if x else None)
        df = df.dropna(axis = 0, subset=['corpus_id', 'title'])
        append_df_to_sql(df, 'papers')
        build_paper_authors(full_papers_df)


def build_paper_authors(full_papers_df):
    paper_author_pairs = []
    def extract_paper_author_pairs(row):
        processed_author_ids = set()
        for author in row['authors']:
            # There were a few duplicate authors in the data
            if author['authorId'] is None or author['authorId'] in processed_author_ids:
                continue

            paper_author_pairs.append({'corpus_id': row['corpusid'], 'author_id': author['authorId']})
            processed_author_ids.add(author['authorId'])

    for index, row in full_papers_df.iterrows():
        pairs = extract_paper_author_pairs(row)
        if pairs is None:
            continue
        paper_author_pairs.extend()
    df = pd.DataFrame(paper_author_pairs)
    df = df.dropna(axis = 0, subset=['corpus_id', 'author_id'])
    append_df_to_sql(df, 'paper_authors')


def insert_abstracts():
    # Abstracts were downloaded in separate files and need to be updated into the papers relation
    # We'd want papers to already be inserted, so that each abstract has a corpus_id to match a paper
    for filename in tqdm(os.listdir(os.path.join(HARDDRIVE_PATH, 'abstracts'))):
        filepath = os.path.join(HARDDRIVE_PATH, 'abstracts', filename)
        if filename.endswith('.zip'):
            continue
        df = pd.read_json(filepath, lines=True)

        engine = create_engine('postgresql://scholar:scholar@localhost/ss_bootstrapping')
        df.to_sql('tmp_table', engine, if_exists='replace')
        sql = '''
        UPDATE papers
        SET abstract = tmp_table.abstract
        FROM tmp_table
        WHERE papers.paper_id = tmp_table.paper_id
        '''
        with engine.begin() as conn:
            conn.execute(sql)



if __name__=='__main__':
    # build_authors()
    build_papers()
    # insert_abstracts()
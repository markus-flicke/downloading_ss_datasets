import os
import pandas as pd
from sqlalchemy import create_engine, bindparam
import sqlalchemy
from tqdm import tqdm

HARDDRIVE_PATH = '/media/scholar/cca30a4f-fb5b-4ec5-9bca-8f51dad1364c/'
SQL_ENGINE_STRING = 'postgresql://scholar:scholar@localhost/ss_bootstrapping'

def append_df_to_sql(df, table_name):
    engine = create_engine(SQL_ENGINE_STRING)
    df.to_sql(table_name, engine, if_exists='append', index=False)


def bind_list_params(query, **kwargs):
    query = sqlalchemy.text(query)

    params = {}
    for key, value in kwargs.items():
        params[key] = value
        if isinstance(value, list):
            query = query.bindparams(bindparam(key, expanding=True))
    return query, params

def sql_execute(query, sql_connection, **kwargs):
    """
    Executes an SQL statement on the gmailgooglescholar database.
    :param query: string
    :return:
    """
    query, params = bind_list_params(query, **kwargs)
    result_proxy = sql_connection.execute(query, params)
    if result_proxy.returns_rows:
        res = result_proxy.fetchall()
        result_proxy.close()
    else:
        res = None
    return res

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
    import pickle as pkl
    with open('global_counts.pkl', 'rb') as f:
        citation_counts = pd.DataFrame(pkl.load(f))

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
        df = df[['corpus_id', 'title', 'publication_date', 'url', 'journal', 'venue', 'year', 'authors']]
        df['abstract'] = None
        df['journal'] = df['journal'].apply(lambda x: x['name'] if x else None)
        df = df.dropna(axis = 0, subset=['corpus_id', 'title'])
        df['authors'] = df['authors'].apply(lambda row: [author['name'] for author in row])

        # build_paper_authors(full_papers_df) # don't need this when we just drop papers relation
        # add citation counts
        def get_citation_count(corpus_id):
            try:
                return citation_counts.loc[corpus_id].values[0]
            except KeyError:
                return 0
        df['citation_count'] = df['corpus_id'].apply(get_citation_count)
        append_df_to_sql(df, 'papers')



def build_paper_authors(full_papers_df):
    paper_author_pairs = []
    def extract_paper_author_pairs(row):
        processed_author_ids = set()
        if row['authors'] is None:
            return None
        

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

    df = pd.DataFrame(paper_author_pairs)
    df = df.dropna(axis = 0, subset=['corpus_id', 'author_id'])
    append_df_to_sql(df, 'paper_authors')


def insert_abstracts():
    # Abstracts were downloaded in separate files and need to be updated into the papers relation
    # We'd want papers to already be inserted, so that each abstract has a corpus_id to match a paper
    for filename in tqdm(os.listdir(os.path.join(HARDDRIVE_PATH, 'abstracts', 'shards'))):
        filepath = os.path.join(HARDDRIVE_PATH, 'abstracts', 'shards', filename)
        if filename.endswith('.zip'):
            continue
        df = pd.read_json(filepath, lines=True)
        df = df[['corpusid', 'abstract']]
        engine = create_engine(SQL_ENGINE_STRING)
        df.to_sql('tmp_table', engine, if_exists='replace')
        sql = '''
        UPDATE papers
        SET abstract = tmp_table.abstract
        FROM tmp_table
        WHERE papers.corpus_id = tmp_table.corpusid
        '''
        print(sql)
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text(sql))

def add_citation_counts(counts):
    engine = create_engine(SQL_ENGINE_STRING)
    counts = counts.reset_index()
    counts.to_sql('tmp_table', engine, if_exists='replace')
    sql = '''
    UPDATE papers
    SET citation_count = citation_count + tmp_table.count
    FROM tmp_table
    WHERE papers.corpus_id = tmp_table.cited_corpus_id
    '''
    print(sql)
    with engine.begin() as conn:
        conn.execute(sqlalchemy.text(sql))


def insert_citations():
    import pickle
    filenames = os.listdir(os.path.join(HARDDRIVE_PATH, 'citations', 'shards'))
    filenames = sorted(filenames)
    global_counts = None
    for filename in tqdm(filenames):
        filepath = os.path.join(HARDDRIVE_PATH, 'citations', 'shards', filename)
        if filename.endswith('.gz'):
            continue
        df = pd.read_json(filepath, lines=True)
        df = df[['citingcorpusid', 'citedcorpusid']]
        df = df.rename(columns={'citingcorpusid': 'citing_corpus_id',
                                'citedcorpusid': 'cited_corpus_id',
                                })
        df = df.dropna(axis = 0, subset=['citing_corpus_id', 'cited_corpus_id'])
        df = df.set_index('citing_corpus_id', drop=True)
        if global_counts is None:
            global_counts = df.value_counts('cited_corpus_id')
        else:
            global_counts = global_counts.add(df.value_counts('cited_corpus_id'), fill_value=0)
        
        with open('global_counts.pkl', 'wb') as f:
            pickle.dump(global_counts, f)
        

    



if __name__=='__main__':
    # insert_citations()
    build_papers()
    insert_abstracts()
from read_gz import create_json_generator
from queries import *
from tqdm import tqdm

def get_exisiting_ss_ids():
    query = 'select semantic_scholar_id from papers where semantic_scholar_id is not null'
    db_ss_ids = sql_execute(query)
    db_ss_ids = set([item[0] for item in db_ss_ids])
    return db_ss_ids

def fill_corpus_id():
    import os 
    filenames = os.listdir('/home/scholar/s2orc/papers/papers/')[20:]
    db_ss_ids = get_exisiting_ss_ids()

    for filename in tqdm(filenames):
        if not filename.endswith('.gz'):
            continue

        for i, item in enumerate(create_json_generator(f'/home/scholar/s2orc/papers/papers/{filename}')):
            if item['url'] is None:
                continue
            ss_id = item['url'].lstrip('https://www.semanticscholar.org/paper/')
            if ss_id not in db_ss_ids:
                continue
            corpus_id = item['corpusid']
            query = "UPDATE papers SET corpus_id = :corpus_id WHERE semantic_scholar_id = :ss_id"
            sql_execute(query, corpus_id=corpus_id, ss_id=ss_id)



if __name__ == '__main__':
    fill_corpus_id()
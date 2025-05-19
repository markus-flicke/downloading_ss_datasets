from read_gz import create_json_generator
from queries import *
import pickle
from tqdm import tqdm

def get_exisiting_corpus_ids():
    query = 'select corpus_id from papers where corpus_id is not null'
    db_corpus_ids = sql_execute(query)
    db_corpus_ids = set([item[0] for item in db_corpus_ids])
    return db_corpus_ids

def accumulate_cited_corpus_ids():
    import os 
    filenames = os.listdir('/media/scholar/LarsHD/citations/')
    db_corpus_ids = get_exisiting_corpus_ids()
    res = dict()

    for filename in tqdm(filenames):
        if not filename.endswith('.gz'):
            continue

        for i, item in enumerate(create_json_generator(f'/media/scholar/LarsHD/citations/{filename}')):
            cited_corpus_id = item['citedcorpusid']
            if cited_corpus_id is None or item['citingcorpusid'] is None:
                continue
            if cited_corpus_id not in db_corpus_ids:
                continue

            if cited_corpus_id not in res:
                res[cited_corpus_id] = [item['citingcorpusid']]
            else:
                res[cited_corpus_id].append(item['citingcorpusid'])
            
        with open('res.pkl', 'wb') as f:
            pickle.dump(res, f)



if __name__ == '__main__':
    accumulate_cited_corpus_ids()
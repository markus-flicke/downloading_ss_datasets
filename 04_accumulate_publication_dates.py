from read_gz import create_json_generator
from datetime import date

import os
import pickle

def accumulate_cited_corpus_ids():
    import os 
    filenames = os.listdir('/home/scholar/s2orc/papers/papers/')

    with open('res.pkl', 'rb') as f:
        res = pickle.load(f)

    corpus_ids_to_look_up = []
    corpus_ids_to_look_up.extend(res.keys())
    from tqdm import tqdm
    values = [v for l in res.values() for v in l]
    for values in tqdm(res.values()):
        corpus_ids_to_look_up.extend(values)


    corpus_ids_to_look_up = set(corpus_ids_to_look_up)

    cid_to_date = dict()

    del res


    for filename in tqdm(filenames):
        if not filename.endswith('.gz'):
            continue

        for i in create_json_generator(f'/home/scholar/s2orc/papers/papers/{filename}'):
            corpus_id = i['corpusid']
            if corpus_id not in corpus_ids_to_look_up:
                continue
            if i['publicationdate'] is None:
                continue
            publication_date = date(*[int(v) for v in i['publicationdate'].split('-')])
            cid_to_date[corpus_id] = publication_date
        
        with open('cid_to_date.pkl', 'wb') as f:
            pickle.dump(cid_to_date, f)
accumulate_cited_corpus_ids()
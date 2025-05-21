import pickle
from queries import sql_execute
from tqdm import tqdm


with open('cited_corpus_ids.pkl', 'rb') as f:
    res = pickle.load(f)
    for i in tqdm(res.keys()):
        query = f'update papers set cited_corpus_ids = ARRAY{res[i]} where corpus_id = :corpus_id'
        sql_execute(query, corpus_id=i)
        # print(f'Updated corpus_id {i} with cited_corpus_ids {res[i]}')

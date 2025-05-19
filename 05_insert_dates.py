import pickle

from queries import sql_execute
from tqdm import tqdm
from datetime import date

with open('cid_to_date.pkl', 'rb') as f:
    cid_to_date = pickle.load(f)

query = 'select corpus_id, citing_corpus_ids from papers where corpus_id is not null and citing_corpus_ids is not null'
db_corpus_ids = sql_execute(query)

for row in tqdm(db_corpus_ids):
    corpus_id = row[0]
    citing_corpus_ids = row[1]

    dates = []
    for citing_corpus_id in citing_corpus_ids:
        d = cid_to_date.get(citing_corpus_id)
        if d is not None:
            dates.append(d)
        else:
            dates.append(date(1900, 1, 1)) # my null date
    if dates:
        dates = [str(d) for d in dates]
        query = f'update papers set citing_dates = ARRAY{dates}::DATE[] where corpus_id = :corpus_id'
        sql_execute(query, corpus_id=corpus_id)
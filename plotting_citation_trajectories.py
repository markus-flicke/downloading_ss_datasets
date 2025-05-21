from queries import *
from datetime import date
import matplotlib.pyplot as plt
import numpy as np

train_set_max_date = date(2024, 1, 1)
test_set_max_date = date(2025, 10, 10)

def get_citation_plot_data(corpus_id, test_set=False, data_transform=None):
    query = 'select title, citing_corpus_ids, citing_dates from papers where corpus_id = :corpus_id'
    title, citing_corpus_ids, citing_dates = zip(*sql_execute(query, corpus_id = corpus_id))
    citing_corpus_ids = citing_corpus_ids[0]
    citing_dates = citing_dates[0]


    total_citiations = len(citing_corpus_ids)
    remove_ids = []
    max_date = test_set_max_date if test_set else train_set_max_date

    for i in range(total_citiations):
        if citing_dates[i] == date(1900, 1,1):
            remove_ids.append(i)
            continue
        if citing_dates[i] >= max_date:
            remove_ids.append(i)

    for i in remove_ids[::-1]:
        del citing_dates[i]
        del citing_corpus_ids[i]

    citing_dates, citing_corpus_ids = map(list, zip(*sorted(zip(citing_dates, citing_corpus_ids), key=lambda x: x[0])))
    import pandas as pd
    from datetime import timedelta

    timeseries_index = pd.date_range(start=pd.to_datetime(citing_dates[0]), end=max_date, freq='D', inclusive='left', )
    timeseries_data = pd.Series(index=timeseries_index, data=0)

    for i in range(len(citing_dates)):
        timeseries_data[pd.to_datetime(citing_dates[i])] += 1
    timeseries_data = timeseries_data.cumsum()
    if data_transform is not None:
        timeseries_data = data_transform(timeseries_data)

    if test_set:
        timeseries_data = timeseries_data[timeseries_index >= pd.to_datetime(train_set_max_date)]
        timeseries_index = timeseries_index[timeseries_index >= pd.to_datetime(train_set_max_date)]

    return title, timeseries_index, timeseries_data


def plot_citation_trajectory(ax, corpus_id):
    title, citing_dates, cumulative_citations = get_citation_plot_data(corpus_id)

    ax.scatter(citing_dates, cumulative_citations, s=1)
    ax.set_title(title[0])
    ax.grid()
    ax.set_ylabel('Cumulative Citations')

if __name__ == '__main__':
    print(get_citation_plot_data(201646309, test_set=True))
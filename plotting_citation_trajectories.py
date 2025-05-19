from queries import *
from datetime import date
import matplotlib.pyplot as plt
import numpy as np



def get_citation_plot_data(corpus_id):
    query = 'select title, citing_corpus_ids, citing_dates from papers where corpus_id = :corpus_id'
    title, citing_corpus_ids, citing_dates = zip(*sql_execute(query, corpus_id = corpus_id))
    citing_corpus_ids = citing_corpus_ids[0]
    citing_dates = citing_dates[0]


    total_citiations = len(citing_corpus_ids)
    remove_ids = []
    for i in range(total_citiations):
        if citing_dates[i] == date(1900, 1,1):
            remove_ids.append(i)

    for i in remove_ids[::-1]:
        del citing_dates[i]
        del citing_corpus_ids[i]

    citing_dates, citing_corpus_ids = map(list, zip(*sorted(zip(citing_dates, citing_corpus_ids), key=lambda x: x[0])))
    cumulative_citations = np.arange(1, len(citing_dates) + 1)

    return title, citing_dates, cumulative_citations


def plot_citation_trajectory(ax, corpus_id):
    title, citing_dates, cumulative_citations = get_citation_plot_data(corpus_id)

    ax.scatter(citing_dates, cumulative_citations, s=1)
    ax.set_title(title[0])
    ax.grid()
    ax.set_ylabel('Cumulative Citations')
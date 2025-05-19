import gzip
import json

def create_json_generator(file_path):
    """
    Loads a .gz file, decompresses it, and reads its JSON content.

    Args:
        file_path (str): The path to the .gz file.

    Returns:
        dict or list: The JSON content loaded from the file, or None if an error occurs.
    """

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                try:
                    json_object = json.loads(line.strip())
                    yield json_object
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: '{line.strip()}' - {e}")
    except:
        print(f"Error opening or reading the file: {file_path}")
        return []


def read_all_citations_files():
    import os
    from tqdm import tqdm   
    import pickle
    file_path = '/media/scholar/LarsHD/citations/'  # Replace with the actual path to your .gz file
    filenames = os.listdir(file_path)
    n_skipped_corpus_ids = 0
    res = {}
    for filename in filenames:
        print(filename)
        if filename.endswith('.gz'):
            full_path = os.path.join(file_path, filename)
            for item in tqdm(create_json_generator(full_path)):
                if item['citedcorpusid'] is None:
                    n_skipped_corpus_ids += 1
                    continue
                citingcorpusid = int(item['citingcorpusid'])
                citedcorpusid = int(item['citedcorpusid'])
                if citingcorpusid not in res:
                    res[citingcorpusid] = [item]
                else:
                    res[citingcorpusid].append(citedcorpusid)
        print(len(res))
        with open('res.pkl', 'wb') as f:
            pickle.dump(res, f)
    print(f"Skipped {n_skipped_corpus_ids} corpus IDs.")
    return res

if __name__ == '__main__':
    # Example usage:
    # file_path = '/media/scholar/LarsHD/citations/citations_part1.gz'  # Replace with the actual path to your .gz file
    # json_data = read_gzipped_json(file_path)
    res = read_all_citations_files()
    print(len(res))


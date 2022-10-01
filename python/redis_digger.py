import gzip
import pickle as p
import re
import string
from collections import Counter

import pandas
import pandas as pd
import redis
import xgboost
from hypy_utils import write
from hypy_utils.tqdm_utils import pmap
from xgboost import XGBClassifier

from main import job_start_redis
from pandas import DataFrame
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = p.load(f)
        l = pd.DataFrame(loaded_object)
        return l


# total changed files
# total commits
# total fix commits
# avaerage changed lines per fix
#
def get_root_nodes(date: str):
    result = sorted([])
    for patch in os.listdir(f"../../data.absolute/{date}/patterns"):
        with open(f"../../data.absolute/{date}/patterns/{patch}", 'r') as f:
            result.append(f.readline())
    return sorted(list(set(result)))


def label_gen() -> DataFrame:
    start_string = "2001-12-01"
    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    interval = relativedelta(months=6)

    csv = []

    data_path = Path('../../data.absolute')
    new = get_root_nodes(start_string)
    new = sorted(list(set(new)))
    added = sorted(list(set(new)))
    remove = sorted([])
    csv.append((start_date.strftime('%Y-%m-%d').split(' ')[0], len(new), len(added), len(remove),
                added, remove, True))

    while True:
        #   end = start + interval
        end_date = start_date + interval
        end_string = end_date.strftime('%Y-%m-%d').split(' ')[0]
        start_string = start_date.strftime('%Y-%m-%d').split(' ')[0]
        if not os.path.isdir(data_path / str(end_string)):
            # new = os.listdir(data_path / f"{end_string}/patterns")
            # added = sorted(list(set(new)))
            # remove = sorted([])
            #  csv.append((end_string, len(new), added, remove))
            break

        new = get_root_nodes(end_string)
        old = get_root_nodes(start_string)

        added = sorted(list(set(new) - set(old)))
        remove = sorted(list(set(old) - set(new)))

        csv.append((end_string, len(new), len(added), len(remove), added, remove, len(added) != 0))

        start_date += interval

    # plt.plot([v[1] for v in csv], [v[2] for v in csv])
    # plt.show()

    df = DataFrame(csv, columns=('Time', 'Number of Patches', 'Numbers of added', 'Numbers of removed', 'Patches Added',
                                 'Patches Removed', 'New Pattern'))
    df.to_csv('diff-test-absolute-root-2.csv')
    return df


def get_commits_sha(start: str, end: str, project_name: str) -> DataFrame:
    start_date = datetime.strptime(start, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end_date = datetime.strptime(end, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    commits = load_zipped_pickle(f'/workspace/EECS-Research/data.absolute/{end}/commitsDF/{project_name}-fix.pickle.gz')
    return commits[commits['commitDate'].between(start_date, end_date, inclusive=False)]['commit']


if __name__ == '__main__':
    labels = label_gen()

    date = '2022-06-01'
    job_start_redis(f'/workspace/EECS-Research/data.absolute/{date}/redis', 6399)

    # 1. Load AST diffs
    r = redis.StrictRedis(host='localhost', port=6399, db=0)
    print("Connected to redis!")
    ast_diffs = {k.decode(): v.decode() for k, v in r.hgetall('dump').items()}

    # 2. Load commits
    base_path = Path(f'/workspace/EECS-Research/data.absolute/{date}/commitsDF/')
    commit_pickles = [base_path / str(f) for f in os.listdir(base_path) if f.endswith('-fix.pickle.gz')]
    commits = pandas.concat(pmap(load_zipped_pickle, commit_pickles, desc=f'Loading commits'))

    def get_all_commits_sha(start: str, end: str) -> DataFrame:
        start_date = datetime.strptime(start, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(end, '%Y-%m-%d').replace(tzinfo=timezone.utc)
        df = commits[commits['commitDate'].between(start_date, end_date, inclusive=False)]
        return df

    # 3. Filter AST diffs for each time interval

    # 3.1. Find sha in each AST diff
    AST_KEY_SHA_RE = re.compile(r'[0-9a-f]{6,}_[0-9a-f]{6,}')
    ast_diff_sha = {k: AST_KEY_SHA_RE.findall(k) for k in ast_diffs.keys()}
    tmp_bf = len(ast_diff_sha)
    ast_diff_sha = {k: v[0].split('_') for k, v in ast_diff_sha.items() if v}
    print(f'Ignored {len(ast_diff_sha) - tmp_bf} AST diff entries')
    print(f'Commit sha lengths: {Counter([len(sha) for l in ast_diff_sha.values() for sha in l])}')

    ast_diff_date = {}
    for date_start, date_end in zip(labels['Time'][:-1], labels['Time'][1:]):
        # 3.2. Find all commit sha in the time interval
        print(f'Processing time interval from {date_start} to {date_end}')
        commits_sha = {c[:6] for c in get_all_commits_sha(date_start, date_end)['commit']}
        print(f'Total of {len(commits_sha)} commits in the interval')

        # 3.3. Find AST diff entries with commit sha in this interval
        ast_diffs_in_interval = {k for k, s in ast_diff_sha.items() if all(len(sha) == 6 and sha in commits_sha for sha in s)}
        print(f'Total of {len(ast_diffs_in_interval)} AST diffs in the interval')

        # 3.4. Combine AST diffs and save as one file
        ast_combined = '\n\n'.join(ast_diffs[k] for k in ast_diffs_in_interval)
        write(f'ML/ast-diffs/{date_start}.txt', ast_combined)
        ast_diff_date[date_start] = ast_combined

    # 4. Tokenize / Vectorize

    # 4.1. Remove symbols, numbers
    def tmp_clean(s: str) -> str:
        s = s.replace('@TO@', '').replace('@AT@', '').replace('@LENGTH@', '')
        for c in string.punctuation:
            s = s.replace(c, ' ')
        while '  ' in s:
            s = s.replace('  ', ' ')
        return s
    print('Cleaning AST Diffs')
    ast_diff_date = {k: tmp_clean(v) for k, v in ast_diff_date.items()}

    # 4.2. Vectorize X
    tf = TfidfVectorizer(ngram_range=(1, 4))
    X = [ast_diff_date[t] for t in labels['Time']]
    X = tf.fit_transform(X)
    print('TF-IDF Fitting finished:', X.size)

    # 4.3. Vectorize Y
    y = [v != [] for v in labels['Patches Added']]

    # 5. Train models
    print('#################### Step 5 ####################')
    print('Training random forest model...')
    classifier: XGBClassifier = XGBClassifier(tree_method='gpu_hist', n_estimators=300)
    classifier.fit(X, y)
    print(classifier)



import gzip
import os
import pickle as p
import re
import subprocess
from datetime import datetime, timezone
from operator import itemgetter
from pathlib import Path

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame


def get_root_nodes(date: str, projects):
    result = sorted([])
    for patch in os.listdir(f"../../{projects}/{date}/patterns"):
        with open(f"../../{projects}/{date}/patterns/{patch}", 'r') as f:
            result.append(f.readline())
    return sorted(list(set(result)))


def get_keys_list(dict):
    return list(map(itemgetter(0), dict.items()))


def get_all_commits_sha(repo, start: str, end: str) -> DataFrame:
    start_date = datetime.strptime(start, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end_date = datetime.strptime(end, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    loaded_pickle = (load_zipped_pickle(
        f'{base_path}/{repo}-fix.pickle.gz'))
    df = loaded_pickle[loaded_pickle['commitDate'].between(start_date, end_date, inclusive=False)]

    return df


def get_all_fix_commits_sha(df) -> DataFrame:
    return df[df['fixes'].apply(lambda x: len(x) > 0)]


def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = p.load(f)
        l = pd.DataFrame(loaded_object)

        return l


def get_files(commits_df):
    files = commits_df['files'].to_numpy()
    RE = []
    for filedict in files:
        enum = get_keys_list(filedict)
        RE += enum
    return RE


def get_fix_files(commits_df):
    files = commits_df['files'].to_numpy()
    NFCPC = []
    RE = []
    for filedict in files:
        enum = get_keys_list(filedict)
        NFCPC.append(len(enum))
        RE += enum
    return RE, NFCPC


def get_change_loc(project, sha_1, sha_2):
    result = [0, 0, 0, 0]
    # files, add, remove, chrun
    # print(f'location: /workspace/EECS-Research/data-source/repos/{project}')
    # print(f'git diff --stat {sha_1} {sha_2}')
    status = subprocess.check_output(f'git diff --stat {sha_1} {sha_2}',
                                     cwd=f"/workspace/EECS-Research/data-source/repos/{project}",
                                     shell=True).decode().splitlines()
    if (len(status) == 0):
        return result
    status = status[len(status) - 1]
    insertion = re.findall(r'\d+ insertions', status)
    deletions = re.findall(r'\d+ deletions', status)
    files = re.findall(r'\d+ file', status)
    # print(files)
    result[0] = int(files[0].split(' ')[0])
    if len(insertion) != 0:
        result[1] = int(insertion[0].split(' ')[0])
    if len(deletions) != 0:
        result[2] = int(deletions[0].split(' ')[0])
        # print(result)
    result[3] = int(result[1]) - int(result[2])
    return result


if __name__ == '__main__':
    datasets = 'data-all.absolute'
    name = datasets
    # name = 'test'
    print("fuck")
    date = '2001-06-01'
    base_path = Path(f'/workspace/EECS-Research/{datasets}/{date}/commitsDF/')

    start_date = datetime.strptime(date, '%Y-%m-%d')
    interval = relativedelta(months=6)
    repos = [str(f).replace('-fix.pickle.gz', '') for f in os.listdir(base_path) if f.endswith('-fix.pickle.gz')]
    # repos = ['commons-compress']
    features = []
    while True:
        #   end = start + interval
        end_date = start_date + interval
        end_string = end_date.strftime('%Y-%m-%d').split(' ')[0]
        start_string = start_date.strftime('%Y-%m-%d').split(' ')[0]

        if not os.path.isdir(Path(f'/workspace/EECS-Research/{datasets}/{end_string}/commitsDF/')):
            # new = os.listdir(data_path / f"{end_string}/patterns")
            # added = sorted(list(set(new)))
            # remove = sorted([])
            #  csv.append((end_string, len(new), added, remove))
            break

        total_commits = 0
        total_files = []
        total_fix_files = []
        total_files_each_fix = []
        total_author = []
        total_add_loc = []
        total_del_loc = []
        total_churn = []
        total_commits_fix = 0
        for repo in repos:

            # print(f'processing {repo}, bewtween {start_string}, {end_string}')

            commits_timeframe = get_all_commits_sha(repo, start_string, end_string)
            # print(commits_timeframe)
            commits_fix = get_all_fix_commits_sha(commits_timeframe)
            total_commits_fix += len(commits_fix)
            # print(commits_fix)
            # print(len(commits_fix))
            # print(commits_sha)
            if len(commits_timeframe) == 0:
                continue
            commits_sha = commits_timeframe['commit'].to_numpy()
            for i in range(1, len(commits_sha)):
                locs = get_change_loc(repo, commits_sha[i - 1], commits_sha[i])
                total_add_loc.append(locs[1])
                total_del_loc.append(locs[2])
                total_churn.append(locs[3])
            NR = len(commits_sha)
            total_commits += NR

            # print(NR)
            authors = commits_timeframe['committer'].to_numpy()
            AUTH = []
            for author in authors:
                AUTH.append(author)

            total_author += AUTH
            files = commits_timeframe['files'].to_numpy()
            RE = get_files(commits_timeframe)

            total_files += RE
            if len(RE) != 0:
                NREF = len(RE) / len(set(RE))
            if len(commits_fix != 0):
                files, NFCPC = get_fix_files(commits_fix)
                total_fix_files += files
                total_files_each_fix+=NFCPC
                # print(NREF)
        # print(total_add_loc)
        total_add_loc = np.asarray(total_add_loc)
        total_del_loc = np.asarray(total_del_loc)
        total_files_each_fix = np.asarray(total_files_each_fix)
        total_churn = np.asarray(total_churn)
        TNREF = len(total_files) / len(set(total_files)) if len(total_files) != 0 else len(total_files)
        new = get_root_nodes(end_string, datasets)
        old = get_root_nodes(start_string, datasets)
        added = sorted(list(set(new) - set(old)))
        #print(total_files_each_fix)
        NFIX = len(set(total_fix_files))
        NFEFC = (len(total_fix_files) / total_commits_fix) if total_commits_fix != 0 else 0
        feature = [end_string, total_commits, TNREF, NFIX, total_commits_fix, NFEFC, total_files_each_fix.max(),
                   len(set(total_author)),
                   total_add_loc.mean(), total_add_loc.max(),
                   total_del_loc.mean(), total_del_loc.max(), total_churn.mean(), total_churn.max(), total_churn.min(),
                   len(added) != 0]
        print(feature)
        features.append(feature)
        start_date += interval
    df = pd.DataFrame(features, columns=('Time', 'NR', 'NREF', 'NFIX', 'NCFIX', 'NFEFC_AVG', 'NFEFC_MAX', 'NAUTH',
                                         'LOC_ADD_AVG', 'LOC_ADD_MAX', 'LOC_DEL_AVG', 'LOC_DEL_MAX', 'CHURN_AVG',
                                         'CHURN_MAX',
                                         'CHURN_MIN', 'LABEL'))
    df.to_csv(f'{name}-features.csv')

    # NR: Number of revisions: commits between these timeline
    # NREF Number refreactor each file: totoal changed file/ unique changed file
    # NFIX NUmber of file in bug fix /number of files called 'fix'
    # Nauth number of author who commited , number of authors count by commit
    # LOC_ADD LOC_DEL line  add, removed max,min,avg
    # churn added loc-deleted loc
    # chgser change set number of files , number of files changed per commit, max and average

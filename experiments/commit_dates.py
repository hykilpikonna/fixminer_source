from __future__ import annotations

import os
from datetime import datetime, timezone, date
from pathlib import Path

import numpy as np
import pandas
from matplotlib import pyplot as plt
from pandas import DataFrame

if __name__ == '__main__':
    path = Path('../../data.relative/0/commitsDF')
    project_list=[p.replace('-fix.pickle.gz','') for p in os.listdir(path) if
     p.endswith('pickle.gz')]
    dates_by_repo: list[list[datetime]] = \
        [list(pandas.read_pickle(path / str(p)).commitDate) for p in os.listdir(path) if
         p.endswith('pickle.gz')]
    dates = np.hstack(dates_by_repo)

    plt.hist(dates, bins=50)
    plt.xlabel('Date')
    plt.ylabel('Total Commits')
    plt.xlim([date(2001, 1, 1), date(2022, 6, 1)])
    plt.savefig("fm-dates.png")
    plt.show()


    first_dates = [cs[-1] for cs in dates_by_repo]
    plt.hist(first_dates, bins=20)
    plt.xlabel('First Commit Date')
    plt.xlim([date(2001, 1, 1), date(2022, 6, 1)])
    #plt.show()

    last_dates = [cs[0] for cs in dates_by_repo]
    plt.hist(last_dates, bins=20)
    plt.xlabel('Last Commit Date')
    plt.xlim([date(2001, 1, 1), date(2022, 6, 1)])
    #plt.show()

    mean_dates = [datetime.fromtimestamp(
        float(np.mean([c.replace(tzinfo=timezone.utc).timestamp() for c in cs]))) for cs in
                  dates_by_repo]
    plt.hist(mean_dates, bins=20)
    plt.xlabel('Mean Commit Date')
    plt.xlim([date(2001, 1, 1), date(2022, 6, 1)])
    #plt.show()
    csv = []
    for i in range(len(first_dates)):
        csv.append((project_list[i],first_dates[i], last_dates[i]))
    df = DataFrame(csv, columns=('project','first_dates','last commit dates'))
    df.to_csv('commits-dates.csv')

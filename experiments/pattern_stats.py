import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame


def calculate_stats(date):
    string = date.strftime('%Y-%m-%d').split(' ')[0]
    files = os.listdir(f"../../data.absolute/{string}/patterns")
    array = []

    for file in files:
        t = int(file.split('#')[1])
        print(t)
        array.append(t)
    df = DataFrame(array)
    plt.hist(array)
    plt.savefig(f'figs/{string}.png')
    return [string, len(df), df.mean(), df.median(), df.max()]


if __name__ == '__main__':
    start_string = "2001-06-01"
    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    interval = relativedelta(months=6)
    calculate_stats(start_date)
    csv = []

    data_path = Path('../../data.absolute')
    new = os.listdir(data_path / f"{start_date.strftime('%Y-%m-%d').split(' ')[0]}/patterns")
    added = sorted(list(set(new)))
    remove = sorted([])
    csv.append((calculate_stats(start_date)))

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

        csv.append(calculate_stats(start_date))

        start_date += interval

    # plt.plot([v[1] for v in csv], [v[2] for v in csv])
    # plt.show()
    df = DataFrame(csv, columns=('Time', 'Number of Patches',
                                 'Mean', 'Median', 'Max'
                                 ))
    df.to_csv('Patch-stats-fixminer.csv')

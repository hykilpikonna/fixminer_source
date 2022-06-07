import datetime
import os
import sys
from pathlib import Path

from matplotlib import pyplot as plt
from pandas import DataFrame

if __name__ == '__main__':
    csv = []

    data_path = Path('../data.absolute')

    for date in os.listdir(data_path):
        path = data_path / str(date)

        patterns = os.listdir(path / "patterns")

        csv.append((datetime.datetime.strptime(str(date), '%Y-%m-%d'), len(patterns)))

    csv.sort(key=lambda x: x[0])

    plt.plot([v[0] for v in csv], [v[1] for v in csv])
    plt.ylim([0, 3500])
    plt.ylabel('Number of Patches')
    plt.xlabel('Date')
    plt.show()

    df = DataFrame(csv, columns=('Date', 'Number of Patches'))
    df.to_csv('diff-absolute.csv')

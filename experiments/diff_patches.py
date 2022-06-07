import os
import sys
from pathlib import Path

from matplotlib import pyplot as plt
from pandas import DataFrame

if __name__ == '__main__':
    start = 0
    interval = 90

    csv = []

    data_path = Path('../data.absolute')

    while True:
        end = start + interval

        if not os.path.isdir(data_path / str(end)):
            new = os.listdir(data_path / f"{start}/patterns")
            added = sorted(list(set(new)))
            remove = sorted([])
            csv.append((start, len(new), added, remove))
            break

        new = os.listdir(f"../data/{start}/patterns")
        old = os.listdir(f"../data/{end}/patterns")
        added = sorted(list(set(new) - set(old)))
        remove = sorted(list(set(old) - set(new)))

        csv.append((start, len(new), added, remove))

        start += interval

    plt.plot([v[1] for v in csv], [v[2] for v in csv])
    plt.show()

    # df = DataFrame(csv, columns=('Start Time (days before last commit)', 'Number of Patches', 'Patches Added', 'Patches Removed'))
    # df.to_csv('diff-test.csv')

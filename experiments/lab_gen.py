import os
from datetime import datetime
from pathlib import Path

import hypy_utils
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from pandas import DataFrame


def get_root_nodes(date: str, projects):
    result = sorted([])
    for patch in os.listdir(f"../../{projects}.absolute/{date}/patterns"):
        with open(f"../../{projects}.absolute/{date}/patterns/{patch}", 'r') as f:
            result.append(f.readline())
    return sorted(list(set(result)))


def label_gen(projects='', start_string='2001-12-01', askfinal=0) -> DataFrame:
    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    interval = relativedelta(months=6)

    csv = []

    data_path = Path(f'../../{projects}.absolute')
    new = get_root_nodes(start_string, projects)
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

        new = get_root_nodes(end_string, projects)
        old = get_root_nodes(start_string, projects)

        added = sorted(list(set(new) - set(old)))
        remove = sorted(list(set(old) - set(new)))

        csv.append((end_string, len(new), len(added), len(remove), added, remove, len(added) != 0))

        start_date += interval

    # plt.plot([v[1] for v in csv], [v[2] for v in csv])
    # plt.show()
    plt.plot([hypy_utils.parse_date_only(v[0]) for v in csv], [v[1] for v in csv])
    plt.xlabel('Date')
    plt.ylabel('Patterns')
    plt.savefig(f"{projects}-root.png")
    plt.show()
    df = DataFrame(csv, columns=('Time', 'Number of Patches', 'Numbers of added', 'Numbers of removed', 'Patches Added',
                                 'Patches Removed', 'New Pattern'))
    df.to_csv(f'diff-roots-{projects}.csv')
    #return finial result of all roots
    if askfinal == 0:
        return df
    elif askfinal == 1:
        return new


if __name__ == '__main__':
    bdj = label_gen('data-bdj', '2004-12-01', 1)
    d4j = label_gen('data-d4j', askfinal=1)
    fm = label_gen('data',askfinal=1)
    all = label_gen('data-all')
    #unique_bdj = sorted(list(set(bdj) - set(d4j) - set(fm)))
    #unique_fm = sorted(list(set(fm) - set(d4j) - set(bdj)))
    #unique_d4j = sorted(list(set(d4j) - set(fm) - set(bdj)))
    #print(len(unique_bdj))
    #print(len(unique_fm))
    #print(len(unique_d4j))

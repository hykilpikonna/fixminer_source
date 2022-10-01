import os
from datetime import datetime
from pathlib import Path

from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from pandas import DataFrame

if __name__ == '__main__':
    start_string = "2001-06-01"
    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    interval = relativedelta(months=6)

    csv = []

    data_path = Path('../../data-all.absolute')
    new = [patch.split('#')[0] for patch in
           os.listdir(data_path / f"{start_date.strftime('%Y-%m-%d').split(' ')[0]}/patterns")]
    new = sorted(list(set(new)))
    added = sorted(list(set(new)))
    remove = sorted([])
    csv.append((start_date.strftime('%Y-%m-%d').split(' ')[0], len(new), len(added), len(remove),
                added, remove))

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

        new = [patch.split('#')[0] for patch in
               os.listdir(f"{data_path}/{end_string}/patterns")]
        new = sorted(list(set(new)))
        old = [patch.split('#')[0] for patch in
               os.listdir(f"{data_path}/{start_string}/patterns")]
        old = sorted(list(set(old)))
        added = sorted(list(set(new) - set(old)))
        remove = sorted(list(set(old) - set(new)))

        csv.append((end_string, len(new), len(added), len(remove), added, remove
                    ))

        start_date += interval

    plt.plot([v[0] for v in csv], [v[1] for v in csv])
    plt.xlabel('Date')
    plt.ylabel('Patterns')
    plt.savefig("data-all-dates.png")
    plt.show()

    df = DataFrame(csv, columns=('Time', 'Number of Patches',
                                 'Numbers of added', 'Numbers of removed', 'Patches Added',
                                 'Patches Removed'
                                 ))
    #df.to_csv('diff-test-d4j-absolute-root.csv')

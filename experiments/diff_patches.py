import os
from datetime import datetime
from pathlib import Path

from dateutil.relativedelta import relativedelta
from pandas import DataFrame

if __name__ == '__main__':
    start_string = "2001-06-01"
    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    interval = relativedelta(months=6)

    csv = []

    data_path = Path('../data.absolute')
    new = os.listdir(data_path / f"{start_date.strftime('%Y-%m-%d').split(' ')[0]}/patterns")
    added = sorted(list(set(new)))
    remove = sorted([])
    csv.append((start_date.strftime('%Y-%m-%d').split(' ')[0], len(new),len(added),len(remove), added,remove))

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

        new = os.listdir(f"../data.absolute/{end_string}/patterns")
        old = os.listdir(f"../data.absolute/{start_string}/patterns")
        added = sorted(list(set(new) - set(old)))
        remove = sorted(list(set(old) - set(new)))

        csv.append((end_string, len(new),len(added),len(remove), added,remove
                    ))

        start_date += interval

    # plt.plot([v[1] for v in csv], [v[2] for v in csv])
    # plt.show()

    df = DataFrame(csv, columns=('Time', 'Number of Patches',
                                  'Numbers of added','Numbers of removed','Patches Added', 'Patches Removed'
                                 ))
    df.to_csv('diff-test-absolute.csv')

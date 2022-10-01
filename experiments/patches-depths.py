import os
from datetime import datetime
from pathlib import Path

from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from pandas import DataFrame


def line(project, start_string, depth):
    ## d4j: data-d4j
    ## bdj: data-bdj
    ## fixminer: data

    start_date = datetime.strptime(start_string, '%Y-%m-%d')
    interval = relativedelta(months=6)

    csv = []

    data_path = Path(f'../../{project}.absolute')

    new = [patch.split('#')[0] for patch in
           os.listdir(data_path / f"{start_date.strftime('%Y-%m-%d').split(' ')[0]}/patterns")]
    new = sorted(list(set(new)))
    added = sorted(list(set(new)))
    remove = sorted([])
    csv.append((start_date.strftime('%Y-%m-%d').split(' ')[0], len(new), len(added), len(remove),[])
               )

    while True:
        #   end = start + interval
        new = []
        old = []
        depths = []
        end_date = start_date + interval
        end_string = end_date.strftime('%Y-%m-%d').split(' ')[0]
        start_string = start_date.strftime('%Y-%m-%d').split(' ')[0]
        print(f"processing date {start_string}")
        if not os.path.isdir(data_path / str(end_string)):
            # new = os.listdir(data_path / f"{end_string}/patterns")
            # added = sorted(list(set(new)))
            # remove = sorted([])
            #  csv.append((end_string, len(new), added, remove))
            break

        for file in os.listdir(f"../../{project}.absolute/{end_string}/patterns"):
            with open(f"../../{project}.absolute/{end_string}/patterns/{file}") as myfile:
                head = ''
                maxdepth = int(file.split('#')[1])
                depths.append(maxdepth)
                if maxdepth > depth:
                    head = ''.join([next(myfile) for x in range(depth)])
                else:
                    head = ''.join([next(myfile) for x in range(maxdepth)])
                new.append(head)

        new = sorted(list(set(new)))

        for file in os.listdir(f"../../{project}.absolute/{start_string}/patterns"):
            with open(f"../../{project}.absolute/{start_string}/patterns/{file}") as myfile:
                head = ''
                maxdepth = int(file.split('#')[1])
                if maxdepth > depth:
                    head = ''.join([next(myfile) for x in range(depth)])
                else:
                    head = ''.join([next(myfile) for x in range(maxdepth)])
                old.append(head)

        old = sorted(list(set(old)))
        added = sorted(list(set(new) - set(old)))
        remove = sorted(list(set(old) - set(new)))

        csv.append((end_string, len(new), len(added), len(remove), depths
                    ))

        start_date += interval
    df = DataFrame(csv, columns=('Date', 'Number of Patches',
                                 'Numbers of added', 'Numbers of removed', 'Depths'
                                 ))
    df.to_csv(f'diff-test-{project}-absolute-{depth}.csv')
    return [[v[0] for v in csv], [v[1] for v in csv], [v[4] for v in csv]]


def boxplot(line):
    plt.boxplot(line[2],showfliers=False)
    plt.show()


if __name__ == '__main__':
    project = 'data'
    ## d4j: data-d4j
    ## bdj: data-bdj
    ## fixminer: data
    depth = 15
    start_string = "2001-06-01"
    l1 = line(project, start_string, 1)
    boxplot(l1)

    print(l1)
    l2 = line(project, start_string, 3)
    print(l2)
    l3 = line(project, start_string, 5)
    print(l3)
    plt.plot(l1[0], l1[1], 'r', l2[0], l2[1], 'g', l3[0], l3[1], 'b')
    plt.show()

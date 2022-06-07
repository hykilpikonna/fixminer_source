from __future__ import annotations

import os
import re

from pandas import DataFrame


def stats_by_project(d):
    csv = []
    files = os.listdir(f"../data/{d}/patterns")
    for file in files:
        # count inferred
        with open(f"../data/{d}/patterns/{file}") as f:
            infers=re.search("\(([^\)]+)\)",f.read())
            str=infers.group(0)[1:len(infers.group(0))-1]
            projects = str.split(",")
            occurences: dict[str, int] = {}
            for project in projects:
                p=re.search("^[^_]+(?=_)",project).group(0).strip(' ')
                if occurences.get(p):
                    occurences[p]=occurences[p]+1
                else:
                    occurences[p]=1
            for key in occurences.keys():
                csv.append((file, key, occurences[key]))
    df = DataFrame(csv, columns=('Patch Name', 'Inferred from projects', 'occurrence'))
    df.to_csv(f'../stats-by-project/stats-projects-{d}.csv')


if __name__ == '__main__':
    for i in range (0,5950,90):
        stats_by_project(i)

import os
from datetime import datetime
from pathlib import Path

import hypy_utils
import pandas as pd
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt
from pandas import DataFrame

if __name__ == '__main__':
    csv = pd.read_csv('plot_leaf_data.csv')
    print(csv)
    csv.plot(x='Time', y=['Fixminer','Defects4J','Bugs.jar'])
    #[hypy_utils.parse_date_only(csv.loc[:,"Time"])],csv.loc[:,"Fixminer"],csv.loc[:,"Defects4J"],csv.loc[:,"Bugs.jar"],csv.loc[:,"All"]
    plt.plot()
    plt.xlabel('Date')
    plt.ylabel('Patterns')
    plt.savefig(f"total-leaf.png")
    plt.show()

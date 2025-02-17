from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

@dataclass
class Statistics:
    mean: float
    median: float
    lower_quartile: float
    upper_quartile: float
    iqr: float
    minimum: float
    maximum: float
    count: int
    total: float
    stddev: float

    def get_metric_6(self) -> tuple[float, float, float, float, float, float]:
        return self.mean, self.median, self.minimum, self.maximum, self.lower_quartile, self.upper_quartile

    def print(self, dec: int = 2):
        print(f'> Mean: {round(self.mean, dec)}, Median: {round(self.median, dec)}')
        print(f'> Min: {round(self.minimum, dec)}, Max: {round(self.maximum, dec)}')
        print(f'> Q1: {round(self.lower_quartile, dec)}, Q3: {round(self.upper_quartile, dec)}')
        print(f'> StdDev: {round(self.stddev, dec)}, IQR: {round(self.iqr, dec)}')
        print(f'> N: {self.count}')


def _calc_col_stats_helper(col: np.ndarray) -> tuple[float, float, float, float, float, float, float, int, float, float]:
    q1 = np.quantile(col, 0.25)
    q3 = np.quantile(col, 0.75)
    return (
        float(np.mean(col)),
        float(np.median(col)),
        float(q1),
        float(q3),
        float(q3 - q1),
        float(np.min(col)),
        float(np.max(col)),
        len(col),
        float(np.sum(col)),
        float(np.std(col))
    )


def calc_col_stats(col: np.ndarray | list) -> Statistics:
    """
    Compute statistics for a data column
    :param col: Input column (tested on 1D array)
    :return: Statistics
    """
    if isinstance(col, list):
        col = np.array(col)
    return Statistics(*_calc_col_stats_helper(col))


if __name__ == '__main__':
    txt = Path('action-sizes.log').read_text('utf-8').split('\n')
    nums = [int(line) for line in txt if line.isnumeric()]
    # print(nums)

    calc_col_stats(nums).print()
    plt.hist(nums, bins=50)
    plt.show()


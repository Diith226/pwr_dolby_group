import time
from collections import defaultdict

import numpy as np


class Timer:
    TIMES = defaultdict(list)

    def __init__(self, name, cross_point=50):
        self.name = name
        self.cross_point = cross_point
        self._start_time = -1
        self._end_time = 0

    def __enter__(self):
        self._start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end_time = time.time()
        Timer.TIMES[self.name].append(self._end_time - self._start_time)
        if len(Timer.TIMES[self.name]) > 0 and len(Timer.TIMES[self.name]) % self.cross_point == 0:
            print("{}: {:.4f}".format(self.name, np.mean(Timer.TIMES[self.name])))

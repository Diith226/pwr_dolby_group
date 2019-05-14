import io
import re

import numpy as np


class Dream(io.StringIO):
    def __init__(self, resolution=(10, 10)):
        self.height = resolution[0]
        self.widhth = resolution[1]
        self.loading_table = np.zeros(resolution)
        self.current_row = 0
        self.current_column = 0

    def _fill_row(self, column):
        if self.current_column < column and self.current_row < self.height:
            for i in range(column - self.current_column):
                self.loading_table[self.current_row, self.current_column + i] = 1

    def write(self, a):
        mess = re.findall(r"[0-9]?[0-9]/10", a)
        inner = re.findall(r"Image", a)
        column = True
        if len(inner) is not 0:
            column = False

        if len(mess) is not 0:
            number = int(mess[0].split('/')[0])
            if column:
                self._fill_row(number)
                if number == self.widhth:
                    self.current_row += 1
                    self.current_column = 0
                else:
                    self.current_column = number

    def flush(self) -> None:
        pass

    def get_table(self):
        return self.loading_table

    def done(self):
        if self.current_row == 10:
            return True
        return False

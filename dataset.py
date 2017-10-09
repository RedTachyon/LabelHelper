import numpy as np


class Dataset:
    """
    Holds the data from a single file, allowing to get consecutive chunks.
    """

    def __init__(self, path, chunk_size=1000, step=0):
        self.path = path
        self.chunk_size = chunk_size
        self.step = step

        self._read_data()
        self.max_step = np.ceil(self.data.shape[0] / chunk_size)

    def _read_data(self):
        self.data = np.fromfile(self.path, sep=' ')
        self.data = self.data.reshape((-1, 2), order='F')

    def show(self):
        print(self.data)

    def next_chunk(self):
        if self.step >= self.max_step:
            raise ValueError("The file has ended.")
        chunk = self.data[self.step * self.chunk_size:(self.step + 1) * self.chunk_size]
        self.step += 1
        return chunk

    def set_step(self, val):
        self.step = val

    def reset(self):
        self.step = 0
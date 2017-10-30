import struct
import numpy as np

class PhaseImage:
    '''Class for storing information about phase images'''

    def __init__(self, rows, cols,  header_size = 512,  binary_format = '<H', path = './'):
        self._header_size = header_size
        self._rows = rows
        self._cols = cols
        self._binary_format = binary_format
        self._path = path
        self._data = None

    def __dir__(self):
        return 'PhaseImage({0}, {1})'.format(self._rows, self._cols)    

    def read(self):
        '''Reads and returns infomation from phase image file
        Args: void
        Returns: numpy.array(self._rows + 2, self._cols + 2)
        '''

        if (self._data is None):
            #creates array for data, addional two rows and two cols added, for more convinient work with borders
            self._data = np.zeros((self._rows + 2, self._cols + 2), dtype = 'uint16')

            with open(self._path, 'rb') as binary_file:
                binary_file.seek(self._header_size)
                data_view = memoryview(binary_file.read())

                for i in range(self._rows):
                    bytes_row_index = i *2 * self._cols
                    row_temp = struct.iter_unpack(self._binary_format,\
                    data_view[bytes_row_index : bytes_row_index + 2 * self._cols])

                    for (j, value) in enumerate(row_temp):
                        self._data[i+1, j+1] = value[0]                          

            return self._data
        else:
            return self._data

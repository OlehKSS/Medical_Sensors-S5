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
        self._phase_data = None

        #these values will be used for transformation of int pixels value 
        #into wraped phase in range from -pi to pi
        self._min_pixel_value = 0
        self._max_pixel_value = 0

    @classmethod
    def from_data(cls, data):
        '''Special constructor, creates phase image from numpy array of integers.

        Args:
            phase_data (numpy.arra(rows, cols)): two dimensional array with data.

        Returns:
            PhaseImage: phase image object.    
        '''

        img_shape = data.shape

        if (len(img_shape) != 2):
            raise ValueError('Input array should be two dimensional, got {}'.format(img_shape))

        out_obj = cls(img_shape[0], img_shape[1])
        out_obj._data = data
        out_obj.__get_phase_data__()

        return out_obj


    @classmethod
    def from_phase_data(cls, phase_data):
        '''Special constructor, creates phase image from numpy array of phase image data.

        Args:
            phase_data (numpy.arra(rows, cols)): two dimensional array with phase data.

        Returns:
            PhaseImage: phase image object.    
        '''

        img_shape = phase_data.shape

        if (len(img_shape) != 2):
            raise ValueError('Input array should be two dimensional, got {}'.format(img_shape))

        out_obj = cls(img_shape[0], img_shape[1])
        out_obj.__convert_to_image__(phase_data)

        return out_obj


    def __dir__(self):
        return 'PhaseImage({0}, {1})'.format(self._rows, self._cols)


    def __getitem__(self, coords):
        '''[i, j] operator overloading. Method returns value of phase image pixel 
        by using provided coordinates.

        Args:
            coords (int, int): row, column  coordinates of pixel.

        Returns:
            int: pixel value.    
        '''

        row, col = coords

        return self._data[row, col]


    def __convert_to_image__(self, phase_data):
        '''Methods maps provided phase data to [0, 4095] range.

        Args:
            phase_data (numpy.arra(rows, cols)): two dimensional array with phase data.

        Returns: None    
        '''

        self._phase_data = phase_data
        self._min_pixel_value = 0
        self._max_pixel_value = 4095

        min_phase_value = self._phase_data.min()
        max_phase_value = self._phase_data.max()
        
        length = self._max_pixel_value - self._min_pixel_value
        phase_length = max_phase_value - min_phase_value

        #linear transformation coefficients kx + m = y
        k = length / phase_length
        m = (self._min_pixel_value * max_phase_value - self._max_pixel_value * min_phase_value) / phase_length

        self._data = (self._phase_data * k) + m
        self._data = self._data.astype(int)

        
    def __get_phase_data__(self):
        '''Convert the image to a wrapped image with values between -pi and pi and store it.

        Args: None.

        Returns: None.
         '''
        min_pixel_value = np.max(self._data)
        max_pixel_value = np.min(self._data)
        length = max_pixel_value - min_pixel_value
        self._phase_data = (self._data - (length / 2.)) / (length / 2.) * np.pi

    @property
    def shape(self):
        '''Use the function to retrieve shape of the phase image in form (rows, columns).

        Args: None.
        
        Returns:
            (int, int): shape of the phase image.
        '''
        return (self._rows, self._cols)

    @property
    def data(self):
        '''Function returns read phase image data in integer datatype.

        Args: None.

        Returns: numpy.array(self._rows, self._cols).
        '''

        return self._data

    @property
    def phase_data(self):
        '''Method returns read phase image data, every value lies in range from -pi to pi.

        Args: None.
        Returns: numpy.array(self._rows, self._cols).
        '''
        return self._phase_data    

    def read(self):
        '''Reads and returns infomation from phase image file.

        Args: void.

        Returns: numpy.array(self._rows, self._cols).
        '''

        if (self._data is None):
            #creates array for data
            self._data = np.zeros((self._rows, self._cols), dtype = 'uint16')

            with open(self._path, 'rb') as binary_file:
                binary_file.seek(self._header_size)
                data_view = memoryview(binary_file.read())

                for i in range(self._rows):
                    bytes_row_index = i *2 * self._cols
                    row_temp = struct.iter_unpack(self._binary_format,\
                    data_view[bytes_row_index : bytes_row_index + 2 * self._cols])

                    for (j, value) in enumerate(row_temp):
                        self._data[i, j] = value[0]                          


            #Convert the image to a wrapped image with values between -pi and pi and store it 
            self.__get_phase_data__()

            return self._data
        else:
            return self._data


    def get_phase_of_pxl(self, row, col):
        '''Method returns pixel value converted to a [-pi, pi] range.

        Args:
            row (int): rows of pixel
            col (int): column of pixel

        Returns:
            (float): pixel value in a [-pi, pi] range
        '''

        return  self._phase_data[row, col]
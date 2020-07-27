
filename ='Data_prueba_PI.csv'
file_effiency = 'Effiency_test.csv'

var_delimiter=','
first_label = ''
second_label = ''
third_label = ''
sumx = 0
sumz = 0
n = 0
count_zeros = 0
standard_deviation = 0

FACTOR_CONVERSION_TF_GG = 1000
FACTOR_PERCENT = 100
N_DECIMAL = 4
MAX = 0x3f3f3f3f
arr_eficiencia = []


def resize(array, new_size, new_value=0):
    """Resize to biggest or lesser size."""
    element_size = len(array[0]) #Quantity of new elements equals to quantity of first element
    if new_size > len(array):
        new_size = new_size - 1
        while len(array)<=new_size:
            n = tuple(new_value for i in range(element_size))
            array.append(n)
    else:
        array = array[:new_size]
    return array



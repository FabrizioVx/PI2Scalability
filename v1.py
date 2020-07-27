import matplotlib
from config import *
from matplotlib import pyplot as plt
from matplotlib import style
from functools import lru_cache
from scipy.interpolate import lagrange, interp1d
from math import sqrt
import numpy as np
import linecache as lc
style.use('ggplot')


with open(filename) as f:
    n_ = len(list(f))

#linecache.getline('filename', line_number)
f = open(filename,'r')
first_line = lc.getline(filename,1)
stflops = lc.getline(filename, n_)
x,y,z = np.loadtxt(filename,unpack=True,delimiter=var_delimiter,skiprows=1,max_rows=n_-2)

def eliminate_zeros(z):
    global count_zeros
    array = np.array(z)
    for i in range(0,len(z)):
        if z[i] == 0:
            count_zeros +=1
    array_without_zeros = array[array!=0]
    return array_without_zeros

newz = eliminate_zeros(z)

#Labels
def first_line_tag(first_line):
    line = first_line.split(var_delimiter)
    return line[0]

def second_line_tag(first_line):
    line = first_line.split(var_delimiter)
    return line[1]

def third_line_tag(first_line):
    line = first_line.split(var_delimiter)
    return line[2]

def all_labels(line):
    global first_label
    global second_label
    global third_label
    first_label = first_line_tag(line)
    second_label = second_line_tag(line)
    third_label = third_line_tag(line)

#Regresion lineal y = ax + b
#Obteniendo a
def getA(x,newz):
    sumxy = 0
    sumxx= 0
    global sumx
    global sumz
    global a
    global n
    n = len(x)
    for i in range(0,len(newz+1)):
        sumxy += (x[i]*newz[i])
        sumx +=x[i]
        sumz +=newz[i]
        sumxx += pow(x[i],2)


    ssumx = pow(sumx,2)
    a = (((n*sumxy)-(sumx*sumz))/((n*sumxx)-(ssumx)))
    return round(a,N_DECIMAL)

a = getA(x,z)

#Obteniendo b
def getB():
    aux = (sumz - a*sumx)/n
    return round(aux,N_DECIMAL)

b = getB()



#Definiendo funcion constante + b
@lru_cache(maxsize=1)
def f1(x):
    return x+b
def f2(y):
    return find_min(y)

#Escalabilidad %
def scalability():
    ggflops_prac = float(stflops) * FACTOR_CONVERSION_TF_GG
    ggflops_teo = (ggflops_prac - b) / a
    scalability = (ggflops_teo - ggflops_prac) * FACTOR_PERCENT / ggflops_teo
    print("El porcentaje de escalabilidad es: ",round(scalability, N_DECIMAL), '%')

def find_min(y):
    min_time_execution = MAX
    for i in range(0,len(y)):
        if(y[i] < min_time_execution):
            min_time_execution = y[i]
    return min_time_execution


def show():
    return matplotlib.pyplot.show(block=True)


def first_graph():
    x, y, z = np.loadtxt(filename, unpack=True, delimiter=var_delimiter,max_rows=n_ - 2,skiprows=1)
    f = np.resize(newz, (len(z)) - count_zeros)
    g = np.resize(x, len(x) - count_zeros)
    all_labels(first_line)
    poly = interp1d(g,f,kind='linear')
    plt.plot(poly.x, poly.y, '+', color="red", linewidth="3", label="h(x) = %a x + %a" % (a, b))
    plt.plot(x, [f1(i) for i in x], '^', color="green", label="f(x) = x + %a " % b)
    plt.title(first_label + ' vs ' + third_label)
    plt.ylabel(third_label)
    plt.xlabel(first_label)
    plt.legend()
    scalability()

def second_graph():
    poly = interp1d(x,y,kind='quadratic')
    plt.plot(poly.x, poly.y, '+', color="blue", linewidth="3",label ="Tiempo mínimo de ejecución: %a "% find_min(y))
    #plt.plot(x,find_min(y))
    plt.plot(x,[f2(y) for i in x], '+', color="magenta")
    plt.title(second_line_tag(first_line) + 'vs'+first_line_tag(first_line) )
    plt.ylabel(second_line_tag(first_line))
    plt.xlabel(first_line_tag(first_line))
    plt.legend()
    print("El tiempo mínimo de ejecución es: ",find_min(y),'segundos')

def speed(speed1,speedP):
    return speed1/speedP

def efficiency(speed,x):
    return speed/x


def calculate_efficiency():
    f = open(file_effiency,'w')
    f.write('Procesos,TiempoEjecucion,Eficiencia\n')
    prom_ = 0
    global standard_deviation
    sum_cuadrada = 0
    for i in range(len(x)):
        s = speed(y[0],y[i])
        arr_eficiencia.append(efficiency(s,x[i]))
        prom_ += efficiency(s,x[i])
        f.write(str(round(x[i])) + ',' + str(round(s,N_DECIMAL)) + ',' + str(round(efficiency(s,x[i]),N_DECIMAL)) + '\n')
    prom_ = prom_/(len(x))
    for i in range(len(x)):
        sum_cuadrada += (efficiency(speed(y[0],y[i]),x[i]) - prom_) ** 2
    standard_deviation = sqrt(sum_cuadrada/len(x))
    print("La desviación estandar es: "+str(round(standard_deviation,N_DECIMAL)))
    print("El promedio de eficiencia es: "+str(round(prom_,N_DECIMAL)))

def graph_efficiency():
    plt.plot(x,arr_eficiencia,'*', color="green", linewidth="3",label ="Desviación estándar: %a "%round(standard_deviation,N_DECIMAL))
    plt.xlabel(first_line_tag(first_line))
    plt.ylabel("Eficiencia")
    plt.title("Eficiencia vs Procesos")
    plt.legend()
    plt.show()


def main():
    calculate_efficiency()
    #first_graph()
    graph_efficiency()
    show()
    second_graph()
    show()



if __name__ == "__main__":
    main()



"""
NOTA: Data_prueba_PI.csv es un csv referencial con delimitador ','
que toma como primera columna la cantidad de procesos a graficar
(X),la segunda columna representa el tiempo de ejecucion(Y) la
tercera columna representa la velocidad en GFlops (Z).

CantidadProcesos,TiempoEjecucion,Velocidad(Gflops)
1,11244.12,5.247
2,10212.973,9.659
4,8783.32,10.976
8,6022.1,11.685
16,4012.1,14.002
2.413

Donde:
{CantidadProcesos,TiempoEjecucion,Velocidad(GGflops)} = Nombre etiquetas que se usaran el nombre los ejes de la gráficas
{1,2,4,8,16,32} = Primera columna(Procesos)
{11244.12,10212.973,8783.32,6022.1,4012.1,3427.4} = Segunda Columna(Tiempo de Ejecucion)
{5.247,9.659,10.976,11.685,14.002} = Tercera columna (Velocidad en GFlops)
{2.413} = Representa la velocidad de su computador (En TeraFlops)
NOTA: Si desea realizar cambiar la precisión ir al archivo config.py y modicar la variable N_DECIMAL
"""


import math
from matplotlib import pyplot as plt
def figuras_de_lisajous(velocidad_angular_x, velocidad_angular_y, desplazamiento_y):
    periodo_1 = math.pi*2/velocidad_angular_x
    periodo_2 = math.pi*2/velocidad_angular_x
    if(periodo_1<periodo_2):
        periodo_1=periodo_2
    tiempo = 0
    intervalo_tiempo = periodo_1/1000
    coordenadas_x = []
    coordenadas_y = []
    coordenadas_x.append( (math.sin(velocidad_angular_x * tiempo)))
    coordenadas_y.append((math.sin(velocidad_angular_y * tiempo + desplazamiento_y)))
    while(tiempo == periodo_1):
        tiempo += intervalo_tiempo
        coordenadas_x.append((math.sin(velocidad_angular_x * tiempo)))
        coordenadas_y.append((math.sin(velocidad_angular_y * tiempo + desplazamiento_y)))
    plt.plot(coordenadas_x, coordenadas_y)
    plt.title("Laisajouse")
    plt.show()
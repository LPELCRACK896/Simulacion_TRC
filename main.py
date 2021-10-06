'''
Authors:
@Luis_Aldana
@Fernando
Cathode Ray Tube Simulation (CRT)

'''

'''
Informacion importante
Aceleracion Entre placas: a = abs(q)*V/(md)
'''
import math
import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
import threading

from matplotlib import pyplot as plt

# ------------------------------------#
# ----------Variables fijas-----------#
# ------------------------------------#
tamano_de_pantalla_vertical = 0.126  # en metros, relativo a las medidas obtenidas
tamano_de_pantalla_horizontal = 0.2  # En metros, relatico a las medidas obtenidas
largo_placa_v = 0.1
largo_placa_h = largo_placa_v
distancia_entre_placasV = 0.1
distancia_entre_placasH = 0.1
distancia_entre_placasVH = 0.05
distancia_entre_placaH_pantalla = 0.2
# ------------------------------------#
# Variables controladas por el usuario#
# ------------------------------------#
voltaje_de_aceleracion_de_electrones = 0
voltaje_de_placas_de_deflexion_verticales = 0
voltaje_de_placas_de_deflexion_horizontales = 0
boton_de_cambio_de_modo = False
control_de_senal_sinusoidal = False
tiempo_de_latencia_de_un_punto_en_pantalla = 0

# ------------------------------------#
# Otras vaiables utiles#
# ------------------------------------##
velocidad_rayo_z = 6.5 * pow(10, 6)
carga_electron = -1.6 * (pow(10, -19))  # Referencia: Sear & Zemansky
carga_rayo = carga_electron
masa_rayo = 9.1 * pow(10, -19)
tiempo_etapa_1 = largo_placa_v / velocidad_rayo_z
tiempo_etapa_2 = distancia_entre_placasVH / velocidad_rayo_z
tiempo_etapa_3 = tiempo_etapa_1
tiempo_etapa_4 = distancia_entre_placaH_pantalla / velocidad_rayo_z
potenical_aceptado = 1.2015 * pow(10, 14)
tonalidades_de_rayo = ["#F4ECF7",  '#E8DAEF', '#D2B4DE',
                       '#BB8FCE', '#A569BD', '#8E44AD',
                       '#7D3C98', '#6C3483', '#5B2C6F',
                       '#4A235A']


def calculo_de_movimiento_x(potencial_placa_vertical):
    velocidad_x = abs(carga_rayo) * potencial_placa_vertical * tiempo_etapa_1 / (masa_rayo * distancia_entre_placasV)
    return (0.5 * abs(carga_rayo) * potencial_placa_vertical * pow(tiempo_etapa_1, 2) / (
                masa_rayo * distancia_entre_placasV)) + velocidad_x * (tiempo_etapa_2 + tiempo_etapa_3 + tiempo_etapa_4)


def calculo_de_movimiento_y(potencial_placa_horizontal):
    velocidad_y = abs(carga_rayo) * potencial_placa_horizontal * tiempo_etapa_3 / (masa_rayo * distancia_entre_placasH)
    return (0.5 * abs(carga_rayo) * potencial_placa_horizontal * pow(tiempo_etapa_3, 2) / (
                masa_rayo * distancia_entre_placasH)) + velocidad_y * tiempo_etapa_4


def comprobacion_de_voltaje(potencial_placa_horizontal):
    if not (potenical_aceptado > potencial_placa_horizontal > -potenical_aceptado):
        print(f"El potencial entre las placas deben estar entre -{potenical_aceptado}V y {potenical_aceptado}V")
        return False
    return True


def trayectoria_de_una_particula(potencial_placa_vertical, potencial_placa_horizontal):
    '''

    :param potencial_placa_vertical:
    :param potencial_placa_horizontal:
    :return:
    '''
    if comprobacion_de_voltaje(potencial_placa_horizontal) and comprobacion_de_voltaje(potencial_placa_vertical):
        coordenada_x = calculo_de_movimiento_x(potencial_placa_vertical)
        coordenada_y = calculo_de_movimiento_y(potencial_placa_horizontal)
        coordenadas = [coordenada_x, coordenada_y]
        return coordenadas
    else:
        return [0, 0]


def figuras_de_lisajous(velocidad_angular_x, velocidad_angular_y, desplazamiento_y, continuidad):
    '''

    :param velocidad_angular_x: velocidad angular para MAS en x  Del 1 al 5
    :param velocidad_angular_y: velocidad angular para MAS en y  Del 1 al 6
    :param desplazamiento_y: desplazamiento para movimiento y segun ecuacion en MAS, valores recomendados: 0, pi/4, pi/2, 3pi/4, pi
    :param continuidad: ingresar 100
    :return: void, pero genera grafica
    '''
    '''
    grafica
    '''
    gData = []
    coordenadas_x = []
    gData.append(coordenadas_x)
    coordenadas_y = []
    gData.append(coordenadas_y)
    '''
    Toda la generacion de datos
    '''
    def GetData(out_data):
        '''

        :param out_data: lista con dos posiciones: index 0: lista eje x a graficar; index 1: eje y a graficar
        :return:void
        '''
        '''
         ELECCION DE COLOR
         '''
        latencia = 0
        limite_inferior = 19
        limite_superior = limite_inferior + 21
        if (continuidad < 20):
            print("La continuidad debe ser mayor a 20")
            return
        for r in range(len(tonalidades_de_rayo)):
            if (limite_inferior < continuidad <= limite_superior):
                latencia = r
                break
            limite_inferior += 20
            limite_superior += 20
            if (r == 9):
                latencia = 9

        color = tonalidades_de_rayo[latencia]
        '''
        ELECCIÓN DE PERIODO
        '''
        periodo_1 = math.pi * 2 / velocidad_angular_x
        periodo_2 = math.pi * 2 / velocidad_angular_y
        if (periodo_1 < periodo_2):
            periodo_1 = periodo_2
        '''
        GENERACION DE PUNTOS
        '''
        tiempo = 0
        intervalo_tiempo = periodo_1 / continuidad
        out_data[0].append(calculo_de_movimiento_x(potenical_aceptado*math.cos(velocidad_angular_x * tiempo)))
        out_data[1].append(calculo_de_movimiento_y(potenical_aceptado*math.cos(velocidad_angular_y * tiempo + desplazamiento_y)))
        for i in range(continuidad):
            tiempo += intervalo_tiempo
            out_data[0].append(calculo_de_movimiento_x(potenical_aceptado * math.cos(velocidad_angular_x * tiempo)))
            out_data[1].append(calculo_de_movimiento_y(potenical_aceptado * math.cos(velocidad_angular_y * tiempo + desplazamiento_y)))
            time.sleep(0.1)

    dataCollector = threading.Thread(target= GetData, args=(gData,) )
    dataCollector.start()

    def update_line(num, hl, data):
        dx = np.array(data[0])
        dy = np.array(data[1])
        hl.set_data(dx, dy)
        return hl,

    fig = plt.figure(figsize=(10, 8))
    plt.xlim(-0.21, 0.21)
    plt.ylim(-0.13, 0.13)
    hl, = plt.plot(gData[0], gData[1])
    line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData ),
                                       interval=50, blit=False)
    plt.show()
    dataCollector.join()
figuras_de_lisajous(1, 2, math.pi / 2, 100)
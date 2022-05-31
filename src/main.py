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
# Otras vaiables utiles  #
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
potenical_aceptado_str = "1.2015e14 V"
tonalidades_de_rayo = ["#F4ECF7", '#E8DAEF', '#D2B4DE',
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


def comprobacion_de_voltaje(potencia_placa):
    if not (potenical_aceptado > (potencia_placa) > -potenical_aceptado):
        print(f"El potencial entre las placas deben estar entre -{potenical_aceptado} y {potenical_aceptado}")
        print(f"El potencial ingresado fue, {potencia_placa}")
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


def figuras_de_lisajous(velocidad_angular_x, velocidad_angular_y, desplazamiento_y, continuidad, periodo):
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
        periodo_1 = periodo_1 * periodo_2 * periodo
        '''
        GENERACION DE PUNTOS
        '''
        tiempo = 0
        intervalo_tiempo = periodo_1 / continuidad
        out_data[0].append(calculo_de_movimiento_x(potenical_aceptado * math.cos(velocidad_angular_x * tiempo)))
        out_data[1].append(
            calculo_de_movimiento_y(potenical_aceptado * math.cos(velocidad_angular_y * tiempo + desplazamiento_y)))
        for i in range(continuidad):
            tiempo += intervalo_tiempo
            out_data[0].append(calculo_de_movimiento_x(potenical_aceptado * math.cos(velocidad_angular_x * tiempo)))
            out_data[1].append(
                calculo_de_movimiento_y(potenical_aceptado * math.cos(velocidad_angular_y * tiempo + desplazamiento_y)))
            time.sleep(0.1)

    dataCollector = threading.Thread(target=GetData, args=(gData,))
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
    line_ani = animation.FuncAnimation(fig, update_line, fargs=(hl, gData),
                                       interval=50, blit=False)
    plt.show()
    dataCollector.join()


def grafica_estandar(index_color):
    potencial_placas_verticales = 0
    potencial_placas_horizontales = 0
    color = tonalidades_de_rayo[index_color]
    '''
    grafica
    '''

    def coloca_puntos():
        fig = plt.figure(figsize=(10, 8))
        plt.xlim(-0.21, 0.21)
        plt.ylim(-0.13, 0.13)
        plt.scatter([calculo_de_movimiento_x(potencial_placas_verticales)],
                    [calculo_de_movimiento_y(potencial_placas_horizontales)], c=color)
        plt.show()

    contador = 0
    print("IMPORTANTE!: "
          "A continuacion se pedira una serie de voltajes.Por favor, primero ingrese un numero no una operacion."
          "\n\tEjemplos"
          "\n\t\tCorrecto: 2"
          "\n\t\tIncorrecto: 2*10^11"
          "\n\t\tIncorrecto: 2e11"
          "\nPosterior a ingresar al numero, podra ingresar una exponente para multiplicar el voltaje")
    input("Enter para continuar...")
    potencial_placas_verticales = float(input(
        f"Ingrese la diferencia de potencial entre las placas verticales (debe estar entre -{potenical_aceptado_str} y {potenical_aceptado_str}): "))
    exponente_potencial_placas_verticales = float(
        input("Ingrese el exponente, el potencial sera multiplicado por 10^... "))
    potencial_placas_verticales = potencial_placas_verticales * pow(10, exponente_potencial_placas_verticales)
    potencial_placas_horizontales = float(input(
        f"Ingrese la diferencia de potencial entre las placas horizontales (debe estar entre -{potenical_aceptado_str} y {potenical_aceptado_str}): "))
    exponente_potencial_placas_horizontales = float(
        input("Ingrese el exponente, el potencial sera multiplicado por 10^... "))
    potencial_placas_horizontales = potencial_placas_horizontales * pow(10, exponente_potencial_placas_horizontales)
    if (comprobacion_de_voltaje(potencial_placas_horizontales) and comprobacion_de_voltaje(
            potencial_placas_verticales)):
        print("Cierre la ventana de la grafica para continuar...")
        if (contador == 0):
            contador = 1
        coloca_puntos()


'''

Menu principal

'''
modo_voltajes = True  # Si modo =True (puede cambiar el voltaje), si modo= False senosoidal activado
while True:
    mod = int(
        input("Ingrese el indice del modo que desea activar:\n1) Cambiar voltaje entre placas\n2) Modo Sinusoisal\n "))
    if (mod == 1):
        modo_voltajes = True
        break
    elif (mod == 2):
        modo_voltajes = False
        break
    else:
        print("Ingrese un indice valido (\"1\" o \"2\")")

while True:
    if modo_voltajes:
        '''
        Modo voltajes
        '''
        salir = False
        while not salir:
            brillo_index = 0
            # Eleccion de intensidad del color de dibujo
            while True:
                res = int(input("De 1 a 10 que tan alto desea el voltaje de aceleracion: "))
                if res == 1 or res == 2 or res == 3 or res == 4 or res == 5 or res == 6 or res == 7 or res == 8 or res == 9 or res == 10:
                    brillo_index = res - 1
                    break
                else:
                    print("Ingrese un numero valido de 1 a 10(entero) ")
            # Eleccion de voltajes dentro de funcion
            grafica_estandar(brillo_index)
            # Salida
            while True:
                res = input("Desea cambiar al modo de cambio de voltaje si o no (s/n): ")
                if (res.lower() == "s"):
                    salir = True
                    break
                elif (res.lower() == "n"):
                    salir = False
                    break
                else:
                    print("Ingrese una opcion valida")

    else:
        '''
        Modo sinusoidal
        '''
        salir = False
        while not salir:
            print(
                "Ha ingresado al modo sinusoidal!\nEn funcion de crear alguna figura de Lissajous, ingrese la siguiente info.")
            velocidad_angular_x = 0
            while True:
                print(
                    "Ingrese una de las siguientes opciones para velocidad angular, para aplicar en el voltaje de placas verticales (movimiento en x)")
                velocidad_angular_x_str = input("1) 1\n2) 2\n3) 3\n4) 4\n5) 5\n6) Otra...\n")
                if velocidad_angular_x_str == "1" or velocidad_angular_x_str == "2" or velocidad_angular_x_str == "3" or velocidad_angular_x_str == "4" or velocidad_angular_x_str == "5":
                    velocidad_angular_x = int(velocidad_angular_x_str)
                    break
                elif velocidad_angular_x_str == "6":
                    velocidad_angular_x_str = float(input("Ingrese velocidad personalizada: "))
                    break
                else:
                    print("Ingrese una opcion valida (indices del 1 al 6)")
            velocidad_angular_y = 0
            while True:
                print(
                    "Ingrese una de las siguientes opciones para velocidad angular, para aplicar en el voltaje de placas horizontales (movimiento en y)")
                velocidad_angular_y_str = input("1) 1\n2) 2\n3) 3\n4) 4\n5) 5\n6) Otra...\n")
                if velocidad_angular_y_str == "1" or velocidad_angular_y_str == "2" or velocidad_angular_y_str == "3" or velocidad_angular_y_str == "4" or velocidad_angular_y_str == "5":
                    velocidad_angular_y = int(velocidad_angular_y_str)
                    break
                elif velocidad_angular_y_str == "6":
                    velocidad_angular_y = float(input("Ingrese velocidad personalizada: "))
                    break
                else:
                    print("Ingrese una opcion valida (indices del 1 al 6)")
            desfase = 0
            while True:
                print("Ingrese el indice del desfase que desea: ")
                desfase_str = str(input("1) 0 \n2) pi/4 \n3) pi/2 \n4) 3pi/4 \n5) pi\n"))
                if (desfase_str == "1"):
                    desfase = 0
                    break
                elif (desfase_str == "2"):
                    desfase = math.pi / 4
                    break
                elif (desfase_str == "3"):
                    desfase = math.pi / 2
                    break
                elif (desfase_str == "4"):
                    desfase = 3 * math.pi / 4
                    break
                elif (desfase_str == "5"):
                    desfase = math.pi
                    break
                else:
                    print("ingrese una opcion valida")
            print("Para continuar con el programa cierre la ventana")
            periodo = 1
            figuras_de_lisajous(velocidad_angular_x, velocidad_angular_y, desfase, 200, periodo)
            while True:
                if (str(input(
                        "Si no se termino de formar la figura esperada ingrese \"s\" (si, esta conforme Presione enter)")).lower() == "s"):
                    periodo = periodo * 2
                    figuras_de_lisajous(velocidad_angular_x, velocidad_angular_y, desfase, 200, periodo)
                else:
                    break

            while True:
                res = input("Desea cambiar al modo de cambio de voltaje si o no (s/n): ")
                if (res.lower() == "s"):
                    salir = True
                    break
                elif (res.lower() == "n"):
                    salir = False
                    break
                else:
                    print("Ingrese una opcion valida")
    modo_voltajes = not modo_voltajes
    if input("Ingese \"s\" para salir, enter para continuar: ").lower() == "s":
        break

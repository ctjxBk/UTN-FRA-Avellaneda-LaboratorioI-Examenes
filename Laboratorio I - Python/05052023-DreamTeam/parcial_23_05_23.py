import json
import re
import csv
import os

def abrir_archivo_json(ruta_archivo: str) -> list:
    '''
    recibe un archivo
    devuelve una lista
    '''
    with open(ruta_archivo, "r") as archivo:
        contenido_archivo_json = json.load(archivo)
    return contenido_archivo_json["jugadores"]


def guardar_archivo_json(ruta_archivo, contenido_archivo_json):
    with open(ruta_archivo, "w") as archivo:
        json.dump(contenido_archivo_json, archivo)

def mostrar_menu_principal(lista: list) -> None:
    '''
    recibe una lista
    recibe str
    devuelve opcion elejiga
    '''
    print("\n\t\033[96mMenu opciones: \033[0m")
    print("1- Mostrar jugadores ")
    print("2- Seleccione un jugador para ver sus estadisticas: ")
    print("3- Logros del jugador")
    print("4- Mostrar promedio de puntos por partido del Dream Team")
    print("5- Seleccione un jugador para saber si es miembro del Salon de la Fama")
#    print("6- Mostrar jugador con mas rebotes totales")
    print("6- Jugador con mayor cantidad de rebotes totales")
    print("7- Jugador con mayor cantidad de tiros de campo")
    print("8- Jugador con mayor cantidad de asistencias totales")
    print("9- Ingrese un valor para saber que jugadores promediaron mas puntos por partido que ese valor ")
    print("10- Ingrese un valor para saber que jugadores promediaron mas rebotes por partido que ese valor ")
    print("11- Ingrese un valor para saber que jugadores promediaron mas asistencias por partido que ese valor ")
    print("12- Jugador con la mayor cantidad de robos totales")
    print("13- Jugador con la mayor cantidad de bloqueos totales")
    print("14- Ingrese un valor para saber que jugadores hayan tenido un porcentaje de tiros libres superior a ese valor ")
    print("15- Mostrar el promedio de puntos por partido del equipo, excluyendo al jugador con la menor cantidad de puntos por partido ")
    print("16- Jugador con la mayor cantidad de logros obtenidos")
    print("17- Ingrese un valor para saber que jugadores hayan tenido un porcentaje de tiros triples superior a ese valor ")
    print("18- jugador con la mayor cantidad de temporadas jugadas ")
    print("19- Ingrese un valor y mostrar los jugadores, ordenados por posición en la cancha, que hayan tenido un porcentaje de tiros de campo superior a ese valor ")
    print("20- Salir")

def mostrar_jugadores(lista: list) -> list:
    '''
    recibe una lista y devuelve una lista
    recibe un str
    devuelve lista
    '''
    print("\033[93mLos mejores jugadores de la NBA:\033[0m")
    indice = 1
    mensaje = None
    for jugador in lista:
        mensaje = "\033[92m{0}-\033[0m {1} - \033[92m{2}\033[0m".format(indice, jugador["nombre"], jugador["posicion"])
        indice += 1
        print(mensaje)
    print(" ")
    return lista

def jugadores_que_coinciden(lista: list) -> list:
    '''
    recibe una lista de jugadores coincidentes
    devuelve lista ordenada en Nombre y Posicion del jugador
    '''
    if lista:
        print("Jugadores que coinciden con el patrón:")
        for jugador in lista:
            print("Nombre: \033[91m{0}\033[0m - Posicion: \033[91m{1}\033[0m".format(jugador["nombre"], jugador["posicion"]))
    else:
        print("No se encontraron jugadores que coincidan con el patrón.")
    return lista

def validar_respuesta_si_no(pregunta):
    '''
    recibe una pregunta como str y valida la respuesta
    retorna un booleano True or False
    '''
    while(True):
        respuesta = input(pregunta)
        if re.match(r"^si$", respuesta, re.IGNORECASE):
            return True
        elif re.match(r"^no$", respuesta, re.IGNORECASE):
            return False
        else:
            print("Por favor, responda 'Si' o 'No'.")


def imprimir_estadistica_de_jugador (jugador_seleccionado: dict) -> list:
    '''
    recibe un diccionario y devuelve una lista con las estadisticas de los jugadores seleccionados
    devuelve una lista ordenada
    '''
    print("\nEstadísticas del jugador \033[92m{0}\033[0m:".format(jugador_seleccionado["nombre"]))
    print("Posición: \033[92m{0}\033[0m".format(jugador_seleccionado["posicion"]))

    mensaje = ""
    jugadores_coincidentes = jugador_seleccionado["estadisticas"]
    for clave, valor in jugadores_coincidentes.items():
        mensaje += "{0}: \033[92m{1}\033[0m\n".format(clave, valor)
    print(mensaje)

    while True:
        pregunta_guardar_estadisticas_txt = validar_respuesta_si_no("\033[96mDesea guardar las estadisticas en un archivo CSV?: \033[0m Si/No ")
        if pregunta_guardar_estadisticas_txt:
            while True:
                nombre_de_guardado = input("\033[96mCon qué nombre quiere guardar el archivo?: \033[0m ")
                ruta_archivo = "I:\\workspace_ani\\UTN_Programacion_2023\\Programacion_1\\python\\Programacion_1\\parcial\\primer_parcial_UTN\\{0}.csv".format(nombre_de_guardado)
                if archivo_existe(ruta_archivo):
                    respuesta = validar_respuesta_si_no("\033[91mYA EXISTE ESE ARCHIVO. Quiere reemplazarlo? Si/No: \033[0m")
                    if respuesta:
                        guardar_estadisticas_jugador(jugador_seleccionado, ruta_archivo)
                        break
                    else:
                        continue
                else:
                    guardar_estadisticas_jugador(jugador_seleccionado, ruta_archivo)
                    break
        break

def elegir_jugador(lista: list) -> list:
    '''
    Elige un jugador de una lista y lo guarda en otra lista.
    Devuelve la lista con jugadores seleccionados.
    '''
    while True:
        respuesta = input("\033[96mElija un jugador por su nombre: \033[0m")
        if respuesta.strip():  # Verifica que la entrada no esté vacía después de eliminar los espacios en blanco
            break
        else:
            print("Entrada inválida. Por favor, ingrese un nombre de jugador.\n")
    
    jugadores_coincidentes = []
    patron = r"(?=.*{0}).*{1}".format(respuesta[0], ".*".join(respuesta[1:]))
    for jugador in lista:
        if re.match(patron, jugador["nombre"], re.IGNORECASE):
            jugadores_coincidentes.append(jugador)
    return jugadores_coincidentes

def validar_valor_ingresado(valor_ingresado_txt: str) -> int:
    '''
    Ingresa un valor str, valida lo ingresado y lo castea a int
    Devuelve booleano True|False
    '''

    patron = r"^[+]?[0-9]+$"
    if re.match(patron, valor_ingresado_txt):
        valor_ingresado_int = int(valor_ingresado_txt)
        return valor_ingresado_int


def mostrar_jugadores_coincidentes(lista: list, callback) -> list:
    '''
    recibe una lista
    muestra el menu
    devuelve una lista con la opcion elegida
    '''
    jugadores_coincidentes = elegir_jugador(lista)

    while True:
        if len(jugadores_coincidentes) == 1:
            jugador_seleccionado = jugadores_coincidentes[0]
            #print("\033[92mlista 01\033[0m", jugadores_coincidentes)
            callback(jugador_seleccionado)
            print(" ")
            break
        elif len(jugadores_coincidentes) > 1:
            jugadores_que_coinciden(jugadores_coincidentes)
            #print("\033[92mlista 01\033[0m", jugadores_coincidentes)
            #print("\033[92mlista 02\033[0m", jugadores_coincidentes)
            jugadores_coincidentes = elegir_jugador(jugadores_coincidentes)
            if len(jugadores_coincidentes) == 1:
                jugador_seleccionado = jugadores_coincidentes[0]
                #print("\033[92mlista 02\033[0m", jugadores_coincidentes)
                callback(jugador_seleccionado)
                break
            break
        else:
            print("No hubo coincidencia")
            break

def ordenar_por_posicion(jugadores):
    jugadores_ordenados = sorted(jugadores, key=lambda x: x['posicion'])
    return jugadores_ordenados

def mostrar_logros_jugador(jugador):
    print("Logros de \033[91m{0}\033[0m".format(jugador["nombre"]))
    for logro in jugador["logros"]:
        print("- \033[92m{0}\033[0m".format(logro))

def encontrar_jugador_mas_all_star(jugadores):
    max_all_star = 0
    jugador_mas_all_star = None
    
    for jugador in jugadores:
        logros = jugador["logros"]
        for logro in logros:
            if "veces All-Star" in logro:
                cantidad_all_star = int(logro.split()[0])
                if cantidad_all_star > max_all_star:
                    max_all_star = cantidad_all_star
                    jugador_mas_all_star = jugador["nombre"]
    return jugador_mas_all_star, max_all_star

def es_miembro_salon_fama(jugador):
    if "Miembro del Salon de la Fama del Baloncesto" in jugador["logros"]:
        print("El jugador \033[92m{0}\033[0m es Miembro del Salón de la Fama del Baloncesto".format(jugador["nombre"]))

def mostrar_minimos(lista: list, clave: str) -> list:
    '''
    toma una lista y calcula el minimo
    recibe lista y clave
    devuelve minimo
    '''
    lista_minimo = []
    minimo = None
    jugador_minimo = None
    for jugador in lista:
        if minimo == None or minimo > jugador["estadisticas"][clave]:
            minimo = jugador["estadisticas"][clave]
            jugador_minimo = jugador["nombre"]
    lista_minimo.append(minimo)
    lista_minimo.append(jugador_minimo)
    return lista_minimo

def mostrar_maximos(lista: list, clave: str) -> list:
    '''
    toma una lista, calcula un maximo
    recibe lista y clave
    devuelve el maximo
    '''
    lista_maximos = []
    maximo = None
    jugador_maximo = None
    for jugador in lista:
        if maximo == None or maximo < jugador["estadisticas"][clave]:
            maximo = jugador["estadisticas"][clave]
            jugador_maximo = jugador["nombre"]
    lista_maximos.append(maximo)
    lista_maximos.append(jugador_maximo)
    return lista_maximos

def suma(lista: list, clave: str) -> int|float:
    suma = 0
    for jugador in lista:
        suma += jugador["estadisticas"][clave]
    return suma

def promedio(suma: int|float, lista: list) -> int|float:
    cantidad_lista = len(lista)
    promedio = suma / cantidad_lista
    return promedio

def filtrar_jugadores_por_promedio(lista_jugadores, estadistica):
    os.system("clear")
    while True:
        valor_ingresado_txt = input("Ingrese un número para filtrar los jugadores por su {0}: ".format(estadistica))
        if validar_valor_ingresado(valor_ingresado_txt):
            valor_ingresado = float(valor_ingresado_txt)
            jugadores_promedio_mayor = []

            for jugador in lista_jugadores:
                promedio_estadistica = jugador["estadisticas"][estadistica]
                if promedio_estadistica > valor_ingresado:
                    jugadores_promedio_mayor.append(jugador)

            if len(jugadores_promedio_mayor) > 0:
                os.system("clear")
                print("\n\033[96mJugadores con un {0} mayor a:\033[0m \033[92m{1}\033[0m".format(estadistica, valor_ingresado))
                jugadores_ordenados = sorted(jugadores_promedio_mayor, key=lambda x: x['posicion'])
                for jugador in jugadores_ordenados:
                    print("- Nombre: \033[92m{0}\033[0m".format(jugador["nombre"]))
                    print("  Posición: \033[92m{0}\033[0m".format(jugador["posicion"]))
                    print("  {0}: \033[92m{1}\033[0m".format(estadistica, jugador["estadisticas"][estadistica]))
                    print("--------")
                presione_enter_para_continuar()
                break
            else:
                print("No hay jugadores con un \033[96m{0}\033[0m mayor a \033[96m{1}\033[0m\n".format(estadistica, valor_ingresado))
            presione_enter_para_continuar()
            break
        else:
            print("El valor ingresado no es válido. Por favor, ingrese un número entero o decimal positivo.")


def buscar_mayores_logros():
    pass

def archivo_existe(ruta_archivo):
    return os.path.exists(ruta_archivo) and os.path.isfile(ruta_archivo)

def guardar_estadisticas_jugador(jugador_seleccionado, ruta_archivo):
    with open(ruta_archivo, 'w') as archivo_csv:
        guardador_csv = csv.writer(archivo_csv)

        guardador_csv.writerow(['Nombre','Posicion', 'Temporadas', 'Puntos totales', 'Promedio de puntos por partido',
                                'Rebotes totales', 'Promedio de rebotes por partido', 'Asistencias totales',
                                'Promedio de asistencias por partido', 'Robos totales', 'Bloqueos totales',
                                'Porcentaje de tiros de campo', 'Porcentaje de tiros libres',
                                'Porcentaje de tiros triples'])

        guardador_csv.writerow([jugador_seleccionado['nombre'],
                                jugador_seleccionado['posicion'],
                                jugador_seleccionado['estadisticas']['temporadas'],
                                jugador_seleccionado['estadisticas']['puntos_totales'],
                                jugador_seleccionado['estadisticas']['promedio_puntos_por_partido'],
                                jugador_seleccionado['estadisticas']['rebotes_totales'],
                                jugador_seleccionado['estadisticas']['promedio_rebotes_por_partido'],
                                jugador_seleccionado['estadisticas']['asistencias_totales'],
                                jugador_seleccionado['estadisticas']['promedio_asistencias_por_partido'],
                                jugador_seleccionado['estadisticas']['robos_totales'],
                                jugador_seleccionado['estadisticas']['bloqueos_totales'],
                                jugador_seleccionado['estadisticas']['porcentaje_tiros_de_campo'],
                                jugador_seleccionado['estadisticas']['porcentaje_tiros_libres'],
                                jugador_seleccionado['estadisticas']['porcentaje_tiros_triples']])
    print("\n\033[92mArchivo guardado de manera exitosa\033[0m")
    print("\033[92mRuta del archivo:\033[0m\n {0}".format(ruta_archivo))
    presione_enter_para_continuar()

def presione_enter_para_continuar():
    '''
    no recibe ni devuelve nada, solo queda en espera hasta que se apriete enter
    '''
    input("\n\t\033[93mPresione Enter para continuar...\033[0m")

def ejecutar_opcion(opcion: str, lista_jugadores: list):
    '''
    recibe una opcion en str
    ejecuta la opcion elejida
    '''
    if opcion == "1":
        os.system("clear")
        mostrar_jugadores(lista_jugadores)
        presione_enter_para_continuar()
    elif opcion == "2":
        os.system("clear")
        mostrar_jugadores(lista_jugadores)
        mostrar_jugadores_coincidentes(lista_jugadores, imprimir_estadistica_de_jugador)
    elif opcion == "3":
        os.system("clear")
        mostrar_jugadores(lista_jugadores)
        mostrar_jugadores_coincidentes(lista_jugadores, mostrar_logros_jugador)
        presione_enter_para_continuar()
    elif opcion == "4":
        os.system("clear")
        equipo = {"jugadores": lista_jugadores}
        promedio_puntos_partido = promedio(suma(equipo["jugadores"], "promedio_puntos_por_partido"), equipo["jugadores"])
        print("\tPromedio de puntos por partido del Dream Team es de: \033[92m{0:.2f}\033[0m\n".format(promedio_puntos_partido))
        presione_enter_para_continuar()
    elif opcion == "5":
        os.system("clear")
        mostrar_jugadores(lista_jugadores)
        mostrar_jugadores_coincidentes(lista_jugadores, es_miembro_salon_fama)
        presione_enter_para_continuar()
    elif opcion == "6":
        os.system("clear")
        maximos_rebotes = mostrar_maximos(lista_jugadores, "rebotes_totales")
        print("El Jugador \033[92m{0}\033[0m tiene la mayor cantidad de rebotes con \033[92m{1}\033[0m rebotes totales".format(maximos_rebotes[1], maximos_rebotes[0]))
        presione_enter_para_continuar()
    elif opcion == "7":
        os.system("clear")
        maximos_tiros_campo = mostrar_maximos(lista_jugadores, "porcentaje_tiros_de_campo")
        print("El Jugador \033[92m{0}\033[0m tiene el mayor porcentaje de tiros de campo con \033[92m{1}\033[0m tiros convertidos".format(maximos_tiros_campo[1], maximos_tiros_campo[0]))
        presione_enter_para_continuar()
    elif opcion == "8":
        os.system("clear")
        maximos_asistencias = mostrar_maximos(lista_jugadores, "asistencias_totales")
        print("El Jugador \033[92m{0}\033[0m tiene la mayor cantidad de asistencias con \033[92m{1}\033[0m asistencias totales".format(maximos_asistencias[1], maximos_asistencias[0]))
        presione_enter_para_continuar()
    elif opcion == "9":
        filtrar_jugadores_por_promedio(lista_jugadores, "promedio_puntos_por_partido")
    elif opcion == "10":
        filtrar_jugadores_por_promedio(lista_jugadores, "promedio_rebotes_por_partido")
    elif opcion == "11":
        filtrar_jugadores_por_promedio(lista_jugadores, "promedio_asistencias_por_partido")
    elif opcion == "12":
        maximos_temporadas = mostrar_maximos(lista_jugadores, "robos_totales")
        print("El Jugador \033[92m{0}\033[0m tiene la mayor cantidad de robos con \033[92m{1}\033[0m robos totales".format(maximos_temporadas[1], maximos_temporadas[0]))
        presione_enter_para_continuar()
    elif opcion == "13":
        maximos_bloqueos = mostrar_maximos(lista_jugadores, "bloqueos_totales")
        print("El Jugador \033[92m{0}\033[0m tiene la mayor cantidad de bloqueos con \033[92m{1}\033[0m bloqueos totales".format(maximos_bloqueos[1], maximos_bloqueos[0]))
        presione_enter_para_continuar()
    elif opcion == "14":
        filtrar_jugadores_por_promedio(lista_jugadores, "porcentaje_tiros_libres")
    elif opcion == "15":
        equipo = {"jugadores": lista_jugadores}
        promedio_minimo = mostrar_minimos(lista_jugadores, "promedio_puntos_por_partido")
        suma_con_minimo = suma(lista_jugadores, "promedio_puntos_por_partido")
        suma_sin_minimo = suma_con_minimo - promedio_minimo[0]
        print("Excluyendo a \033[92m{0}\033[0m que tiene \033[92m{1}\033[0m de promedio por partido\nEl promedio total de puntos por partido es: \033[92m{2:.2f}\033[0m".format(promedio_minimo[1], promedio_minimo[0], suma_sin_minimo))
        presione_enter_para_continuar()
    elif opcion == "16":
        jugador_con_mas_all_star, cantidad_all_star = encontrar_jugador_mas_all_star(lista_jugadores)
        print("El jugador \033[92m{0}\033[0m tiene el mayor número de veces All-Star con \033[92m{1}\033[0m veces".format(jugador_con_mas_all_star, cantidad_all_star))
        presione_enter_para_continuar()
    elif opcion == "17":
        filtrar_jugadores_por_promedio(lista_jugadores, "porcentaje_tiros_triples")
    elif opcion == "18":
        maximos_temporadas = mostrar_maximos(lista_jugadores, "temporadas")
        print("El Jugador \033[92m{0}\033[0m tiene la mayor cantidad de temporadas con \033[92m{1}\033[0m temporadas totales".format(maximos_temporadas[1], maximos_temporadas[0]))
        presione_enter_para_continuar()
    elif opcion == "19":
        filtrar_jugadores_por_promedio(lista_jugadores, "porcentaje_tiros_de_campo")
    elif opcion == "20":
        exit
    else:
        print("Opción inválida.")


# # Programa principal
def main():
    lista_jugadores = []
    ruta_archivo = "I:\\workspace_ani\\UTN_Programacion_2023\\Programacion_1\\python\\Programacion_1\\parcial\\primer_parcial_UTN\\dt.json"
    lista_jugadores = abrir_archivo_json(ruta_archivo)
    while True:
        mostrar_menu_principal(lista_jugadores)
        opcion = input("\t\033[96mIngrese la opción deseada:\033[0m ")
        print(" ")
        ejecutar_opcion(opcion, lista_jugadores)
        if opcion == "20":
            break
main()


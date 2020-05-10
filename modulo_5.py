import sqlite3
import pyttsx3
import re

engine = pyttsx3.init()
voices = engine.getProperty('voices')  # a voices se le carga
# un vector con la información de todas las voces
# getPropierty es para obtener información de algo,
# ya sea el volumen o la velocidad con que habla
engine.setProperty('voice', voices[0].id)  # setProperty es para
# cambiar una propiedad, ya sea voz o volumen
volume = engine.getProperty('volume')  # para obtener el volumen actual
engine.setProperty('volume', volume + 1.0)  # cambiar el volumen
rate = engine.getProperty('rate')  # para obtener la velocidad actual
engine.setProperty('rate', rate - 80)  # cambiar la velocidad con que habla


def personas():
    conexion = sqlite3.connect("bd_conocimientos.sqlite3")
    # Conectar a la base de datos
    cursor = conexion.cursor()
    # Seleccionar el cursor para realizar las consulta

    while True:
        print(
             '¿Qué quieres hacer?\n',
             '(1)Registrar una nueva persona\n',
             '(2)Buscar información de una persona\n',
             '(3)Buscar una persona\n',
             '(0)Volver\n',
             'Digita el número correspondiente'
             )
        engine.say("¿Qué quieres hacer?. Digita el número correspondiente")
        engine.runAndWait()
        a = input('Digita un número entero: ')

        if str(a) == '1':
            print('Por favor digita a continuación sus datos:')
            engine.say("Por favor digita a continuación sus datos")
            engine.runAndWait()
            dni = input('DNI: ')
            nombres = input('Nombres: ')
            apellidos = input('Apellidos: ')
            edad = input('Edad: ')
            direccion = input('Dirección: ')
            email = input('E-mail: ')

            try:
                sql = """
                INSERT INTO personas(
                id, nombres, apellidos, edad, direccion, email
                )
                VALUES(?, ?, ?, ?, ?, ?)
                ;
                """  # sql para insertar la persona
                cursor.execute(sql, (dni, nombres, apellidos, edad, direccion, email))
                # Ejecutamos la consulta
                conexion.commit()  # Si todo fue bien hasta ahora, guardamos
                #los cambios en la bd
                print('Persona registrada con éxito')
            except Exception as e: #Si ocurrió un error lo notificamos
                print("Hubo un problema al registrar la persona. \nError: " + str(e))

            continue


        if str(a) == '2':

            cont = 0
            sql = """SELECT *FROM personas"""
            cursor.execute(sql)
            consulta = cursor.fetchall() #La variable consulta se convierte en un vector que 
            #en cada índice contiene un registro de la consulta hecha

            if len(consulta) > 0:
            
                for i in consulta: #imprimimos las personas
                    print('(', cont,')', str(i[0]) + '-' + str(i[1]))
                    cont += 1

                engine.say("Digita el número de la persona que desea buscar")
                engine.runAndWait()
                x = input("Digita el número de la persona que desea buscar: ")

                while True:
                    try:
                        int(x)
                    except:
                        x = input("Digita el número de la persona que desea buscar: ")
                        continue
                    else:
                        if int(x) >= 0 and int(x) <= len(consulta)-1:
                            break
                        x = input("Digita el número de la persona que desea buscar: ")
            
                x = int(x)
                print(
                     'DNI: ' + str(consulta[x][0]),
                     '\nNombres: ' + str(consulta[x][1]),
                     '\nApellidos: ' + str(consulta[x][2]),
                     '\nEdad: ' + str(consulta[x][3]),
                     '\nDirección: ' + str(consulta[x][4]),
                     '\nE-mail: ' + str(consulta[x][5])
                     )
            else:
                print('No existen personas registradas ')
                engine.say("No existen personas registradas")
                engine.runAndWait()

            continue

       
        if str(a) == '3':
            m = input('Digite el DNI: ')
            while True:
                try:
                    int(m)
                except Exception as e:
                    m = input('Digite el DNI: ')
                    continue
                else:
                    break

            sql = """SELECT *FROM personas"""
            cursor.execute(sql)
            consulta = cursor.fetchall()   # La variable consulta se convierte en un vector que 
            # en cada índice contiene un registro de la consulta hecha
            cont = 0
            if len(consulta) > 0:
            
                for i in consulta: #imprimimos las personas
                    cont += 1
                    obj = str(i[0])
                    patron = '^('+str(m)+')'
                    output = re.findall(patron, obj)
                    if len(output) >= 1:
                        print('(', cont,')', str(i[0]) + '-' + str(i[1]))


                engine.say("Digita el número de la persona que desea buscar")
                engine.runAndWait()
                x = input("Digita el número de la persona que desea buscar: ")

                while True:
                    try:
                        int(x)
                    except:
                        x = input("Digita el número de la persona que desea buscar: ")
                        continue
                    else:
                        if int(x) >= 0 and int(x) <= len(consulta)-1:
                            break
                        x = input("Digita el número de la persona que desea buscar: ")
            
                x = int(x)
                print(
                     'DNI: ' + str(consulta[x][0]),
                     '\nNombres: ' + str(consulta[x][1]),
                     '\nApellidos: ' + str(consulta[x][2]),
                     '\nEdad: ' + str(consulta[x][3]),
                     '\nDirección: ' + str(consulta[x][4]),
                     '\nE-mail: ' + str(consulta[x][5])
                     )
            else:
                print('No existen personas registradas ')
                engine.say("No existen personas registradas")
                engine.runAndWait()

            continue




        if str(a) == '0':
            cursor.close() #Cerramos la conexión con el cursor
            conexion.close() #Cerramos la conexión a la bd
            return

        if str(a) != '1' and str(a) != '2' and str(a) != '3' and str(a) != '0':
            print('Digita un número válido')
            engine.say("Digita un número válido")
            engine.runAndWait()
            continue
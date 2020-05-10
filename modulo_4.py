import sqlite3
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


def comprobar():

    comprobante = 1  # Con esta variable comprobamos que
    # en la secuencia de pasos el anterior se haya ejecutado
    # correctamente
    conversaciones = [
                     'Adios', 'Adios',
                     'Adios', 'Hasta luego',
                     'Hola', 'Hola',
                     'Hola', 'Hola desconocido'
                     ]  # Conversaciones básicas necesarias
    print('Examinando base de conocimientos...')

    if os.access('bd_conocimientos.sqlite3', os.W_OK) == False:  # Revisa si el
        # archivo existe y se puede escribir.
        # Si no existe o no se puede escribir en el, entonces lo creamos.

        print('Base de conocimientos existe [NO]')
        print('Creando base de conocimientos...')

        try:
            f = open('bd_conocimientos.sqlite3', 'w')
            # Creamos el archivo para la bd conocimientos
            f.close()
            print('  -> Creación de la base de conocimientos (OK)')
        except Exception as e:  # Si algo falla, reportamos el error y
            # colocamos en 0 a la variable comprobante para que no se ejecuten
            # el resto de pasos
            comprobante = 0
            print('  -> Creación de la base de conocimientos (X)')
            print("Ha ocurrido un error. \nError: " + str(e))

        conexion = sqlite3.connect("bd_conocimientos.sqlite3")
        # Luego de crear el archivo conectamos a la bd conocimientos.
        cursor = conexion.cursor()
        # Seleccionamos el cursor para realizar las consulta

        if comprobante == 1:  # Si el paso anterior se ejecutó sin problemas

            sql = """CREATE TABLE IF NOT EXISTS conversaciones(
                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  frase VARCHAR(100) NOT NULL,
                  respuesta VARCHAR(100) NOT NULL
                  );
                  """  # sql para tabla de conversaciones

            try:
                cursor.execute(sql)  # Creamos la tabla de conversaciones
                print('  -> Creación de la tabla conversaciones (OK)')
            except Exception as e:  # Si algo falla, reportamos el error y
                # colocamos en 0 a la variable comprobante para que no se
                # ejecuten el resto de pasos
                comprobante = 0
                print('  -> Creación de la tabla conversaciones (X)')
                print("Ha ocurrido un error. \nError: " + str(e))

        if comprobante == 1:  # Si el paso anterior se ejecutó sin problemas

            sql = """CREATE TABLE IF NOT EXISTS personas(
                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  nombres VARCHAR(30) NOT NULL,
                  apellidos VARCHAR(30) NOT NULL,
                  edad VARCHAR(11) NOT NULL,
                  direccion VARCHAR(30) NOT NULL,
                  email VARCHAR(30) NOT NULL
                  );
                  """  # sql para tabla de personas

            try:
                cursor.execute(sql)  # Creamos la tabla de personas
                print('  -> Creación de la tabla personas (OK)')
            except Exception as e:  # Si algo falla, reportamos el error y
                # colocamos en 0 a la variable comprobante para que no se
                # ejecuten el resto de pasos
                comprobante = 0
                print('  -> Creación de la tabla personas (X)')
                print("Ha ocurrido un error. \nError: " + str(e))

        if comprobante == 1:  # Si el paso anterior se ejecutó sin problemas

            sql = """CREATE TABLE IF NOT EXISTS preguntas(
                  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  pregunta VARCHAR(100) NOT NULL
                  );
                  """  # sql para la tabla de preguntas
            try:
                cursor.execute(sql)  # Creamos la tabla de preguntas
                print('  -> Creación de la tabla preguntas (OK)')
            except Exception as e:  # Si algo falla, reportamos el error y
                # colocamos en 0 a la variable comprobante para que no se
                # ejecuten el resto de pasos
                comprobante = 0
                print('  -> Creación de la tabla preguntas (X)')
                print("Ha ocurrido un error. \nError: " + str(e))

        if comprobante == 1:  # Si el paso anterior se ejecutó sin problemas

            sql = """INSERT INTO conversaciones(
                  frase,
                  respuesta
                  )
                  VALUES (?, ?),
                         (?, ?),
                         (?, ?),
                         (?, ?)
                  ;
                  """  # Consulta para insertar las conversaciones
            # básicas necesarias

            try:
                cursor.execute(sql, conversaciones)  # insertamos las
                # conversaciones básicas necesarias
                chatbot = ChatBot('Terminal')  # Llamamos al bot para
                # trabajar con él
                trainer = ListTrainer(chatbot)  # Le asignamos a la
                # variable "trainer"
                # la función de entrenar al bot
                cont = 0
                i = 0
                while cont < len(conversaciones) / 2:  # Entrenamos las
                    # conversaciones báscias necesarias
                    trainer.train([
                                  conversaciones[i],
                                  conversaciones[i + 1]
                                  ])
                    i += 2
                    cont += 1
                trainer.train("chatterbot.corpus.spanish")  # Le entrenamos el
                # chatterbot.corpus.spanish

                print("""  -> Almacenamiento y aprendizaje de
                     conversaciones prediseñadas (OK)""")

            except Exception as e:  # Si algo falla, reportamos el error y
                # colocamos en 0 a la variable comprobante para que no se
                # ejecuten el resto de pasos
                comprobante = 0
                print("""  -> Almacenamiento y aprendizaje de
                     conversaciones prediseñadas (X)""")
                print("Ha ocurrido un error. \nError: " + str(e))

        if comprobante == 1:  # Si los pasos anteriores se ejecutaron con éxito
            # guardamos los cambios en la BD y cerramos la conexión, además
            # retornamos 1 para indicar que el bot está listo

            conexion.commit()  # Guardamos los cambios
            cursor.close()  # Cerramos la conexión con el cursor
            conexion.close()  # Cerramos la conexión a la bd
            print('Base de conocimientos lista para trabajar')
            return 1

        else:  # Si algún paso salió mal, cerramos la conexión
            # sin guardar cambios y eliminamos la bd conocimientos
            # junto a la del bot, además retornamos 0 para indicar
            # que el bot no está listo
            cursor.close()  # Cerramos la conexión con el cursor
            conexion.close()  # Cerramos la conexión a la bd
            chatbot.storage.drop()  # Esto limpia la base de
            # conocimientos del bot
            print('No se puede trabajar con la base de conocimientos')
            return 0

    else:  # Si el archivo de bd conocimientos existe, y se puede
        # escribir sobre él comprobamos que las tablas y las
        # conversaciones básicas necesarias existan
        conexion = sqlite3.connect("bd_conocimientos.sqlite3")
        # Conectar a la base de datos
        cursor = conexion.cursor()  # Seleccionar el cursor
        # para realizar las consulta

        print('Base de conocimientos existe [SI]')
        print('Examinando tablas...')

        sql = """
              SELECT *FROM conversaciones, preguntas, personas;
              """  # sql para consultar si existen las tablas

        try:
            cursor.execute(sql)  # Ejecutamos la consulta
            print("Tablas existen [SI]")
        except Exception as e:  # Si marca un error significa que
            # alguna o ambas tablas no existen
            comprobante = 0
            print("Tablas existen [NO]")
            print("Ha ocurrido un error. \nError: " + str(e))

        if comprobante == 1:  # Si el paso anterior se ejecutó con éxito

            sql = """
                  SELECT *FROM conversaciones
                  WHERE frase = ? AND respuesta = ?
                  UNION
                  SELECT *FROM conversaciones
                  WHERE frase = ? AND respuesta = ?
                  UNION
                  SELECT *FROM conversaciones
                  WHERE frase = ? AND respuesta = ?
                  UNION
                  SELECT *FROM conversaciones
                  WHERE frase = ? AND respuesta = ?
                  ;
                  """  # sql para consultar las conversaciones
            # básicas necesarias

            cursor.execute(sql, conversaciones)  # Ejecutamos la consulta
            consulta = cursor.fetchall()  # La variable consulta almacenará
            # los registros obtenidos
            num_registros = len(consulta)  # Obtenemos la longitud
            # de la consulta

            if num_registros >= 4:  # Si la longitud de la consulta
                # obtenida es igual a 4, significa que las 4 conversaciones
                # básicas necesarias están

                print(' -> Diálogos para saludar y despedirse (OK)')
            else:
                comprobante = 0
                print(' -> Diálogos para saludar y despedirse (X)')

        if comprobante == 1:  # Si los pasos anteriores fueron
            # ejecutados con éxito, cerramos la conexión a la bd y
            # notificamos que el bot está listo para trabajar, y
            # retornamos 1 para indicar que el bot está listo

            cursor.close()  # Cerramos la conexión con el cursor
            conexion.close()  # Cerramos la conexión a la bd
            print('Base de conocimientos lista para trabajar')
            return 1

        else:  # Si los pasos anteriores fueron
            # ejecutados sin éxito, cerramos la conexión a la bd y
            # notificamos que el bot no está listo para trabajar, y
            # retornamos 0 para indicar que el bot no está listo
            cursor.close()  # Cerramos la conexión con el cursor
            conexion.close()  # Cerramos la conexión a la bd
            print('No se puede trabajar con la base de conocimientos')
            return 0

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyttsx3 
import os
import sqlite3
import shutil #Para manejar archivos

 
engine = pyttsx3.init()
voices = engine.getProperty('voices') #a voices se le carga un vector con la información de todas las voces
#getPropierty es para obtener información de algo, ya sea el volumen o la velocidad con que habla
engine.setProperty('voice', voices[0].id) #setProperty es para cambiar una propiedad, ya sea voz o volumen
volume = engine.getProperty('volume') #para obtener el volumen actual
engine.setProperty('volume', volume + 1.0)#cambiar el volumen
rate = engine.getProperty('rate')#para obtener la velocidad actual
engine.setProperty('rate', rate - 80)#cambiar la velocidad con que habla



chatbot = ChatBot('Terminal') 



trainer = ListTrainer(chatbot) 



def aprendizaje2(frase, respuesta_erronea): 

    conexion = sqlite3.connect("bd_conocimientos.sqlite3") #Conectar a la base de datos
    cursor = conexion.cursor() #Seleccionar el cursor para realizar las consulta 

    sql = """SELECT * FROM conversaciones;"""
    cursor.execute(sql)
    consulta = cursor.fetchall() 
    conversaciones = []
    for i in consulta:
        conversaciones.append(i[1]) 
        conversaciones.append(i[2])
 
    #Obtemos las conversaciones que ha aprendido

    
    print(
         "Bot: Perdón, no soy experto en el lenguaje natural." + 
         " Digita la frase adecuada para responder a: ", 
         frase
         )
    engine.say("Perdón, no soy experto en el lenguaje natural.")
    engine.say("Digita la frase adecuada para responder a: ", frase)
    engine.runAndWait()
    respuesta = input('Corrección: ')
    
    indice = conversaciones.index(frase) #Obtenemos la ubicación de la conversación erronea para modificarla
    conversaciones[indice + 1] = respuesta #Este vector es con el cuál le enseñaremos al bot nuevamente
    #las conversaciones que ya sabía, y acá modificamos la conversación erronea

    try:
        sql = """
              UPDATE conversaciones 
              SET respuesta = ? 
              WHERE frase = ? AND respuesta = ? AND id > 0
              ;
              """ #Se debe usar la primary key para modificar una consulta, 
              #esto se puede cabiar en la configuración del gestor de bd.

        #Modificamos la conversación que respondía mal el bot      
        cursor.execute(sql, (str(respuesta), str(frase), str(respuesta_erronea)))

        shutil.copy2('db.sqlite3', 'db1.sqlite3') #Copiamos el archivo (incluidos metadatos), 
        #por si falla el proceso

        chatbot.storage.drop() #Esto limpia la base de conocimientos del bot para entrenarlo de cero


        conversacion1 = [
                        'Adios', 'Adios', 
                        'Adios', 'Hasta luego',
                        'Hola', 'Hola',
                        'Hola', 'Hola desconocido'
                        ]
        cont = 0
        i = 0
        while cont < len(conversacion1) / 2:
            trainer.train([
            conversacion1[i],
            conversacion1[i + 1]    
            ])
            i += 2 
            cont += 1

        #Entrenamos las conversaciones básicas necesarias


        cont = 0
        i = 0
        while cont < len(conversaciones) / 2:
            trainer.train([
            conversaciones[i],
            conversaciones[i + 1]    
            ])
            i += 2 
            cont += 1    

        #Le entrenamos nuevamente todo lo que aprendió


        trainer.train("chatterbot.corpus.spanish") #Le entrenamos el chatterbot.corpus.spanish

        print("Bot: Gracias por corregirme")
        engine.say("Gracias por corregirme")
        engine.runAndWait()



        conexion.commit() #Guardamos cambios en la bd 
        cursor.close() #Cerramos la conexión con el cursor
        conexion.close() #Cerramos la conexión a la bd
        os.remove('db1.sqlite3') #Si todo fue bien, eliminamos la copia

    except Exception as e:
        print("Hubo un problema al modificar la conversación. \nError: " + str(e))
        os.remove('db.sqlite3') #Si algo falló, eliminamos la bd
        os.rename('db1.sqlite3', 'db.sqlite3') #Y restauramos la copia




    return
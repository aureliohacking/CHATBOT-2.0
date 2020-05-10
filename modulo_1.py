from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyttsx3
import datetime
import random
import sqlite3
 

   
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


def aprendizaje1(frase, hora_de_inicio):

    conexion = sqlite3.connect("bd_conocimientos.sqlite3") #Conectar a la base de datos
    cursor = conexion.cursor() #Seleccionar el cursor para realizar las consulta
    
    preguntas = []
    sql = """SELECT *FROM preguntas;"""
    cursor.execute(sql)
    consulta = cursor.fetchall()
    for i in consulta: 
        preguntas.append(i[1]) 
    #Consultamos las preguntas sin responder, más adelante se usan    
    len_preguntas = len(preguntas) #Con ésta variable verificamos más
    #adelante si hay preguntas para hacer, no se coloca después de la inserción
    #de una nueva pregunta, pues ésta no se ha podido responder, así que no
    #podemos preguntar dos veces si se sabe la respuesta, por la misma razón se toma
    #antes la consulta de las preguntas, y no después.


    print("Bot: Lo siento, no entendí \n¿Puedes explicarme qué respuesta dar a tal conversación?")
    engine.say("Lo siento, no entendí. ¿Puedes explicarme qué respuesta dar a tal conversación?")
    engine.runAndWait()

    aux = input('Si = S \nNo = Cualquier caracter\n-->')

    if(str(aux) == 'S' or str(aux) == 's'):

        print("Bot: Digita la frase adecuada para responder a: ", frase)
        engine.say("Digita la frase adecuada para responder a: ", frase)
        engine.runAndWait()
        respuesta = input('Respuesta: ')

        try:
            sql = """INSERT INTO conversaciones(
                  frase,
                  respuesta
                  )
                  VALUES (?, ?)
                  ;
                  """ #sql para insertar la nueva conversación
            cursor.execute(sql, (frase, respuesta)) #Ejecutamos la consulta

            trainer.train([ 
            frase,
            str(respuesta)
            ]) #Entrenamos la nueva conversación al bot

            conexion.commit() #Si todo fue bien hasta ahora, guardamos
            #los cambios

            print("Bot: Aprendido")
            engine.say("Aprendido")
            engine.runAndWait()
            return hora_de_inicio #La función siempre retorna la hora actual

        except Exception as e: #Si ocurrió algún error lo notificamos
            print("Hubo un problema al entrenar el bot. \nError: " + str(e)) 

        
        cursor.close() #Cerramos la conexión con el cursor
        conexion.close() #Cerramos la conexión a la bd
        return hora_de_inicio #La función siempre retorna la hora actual

    else: #Si no saben la respuesta a tal conversación, entonces la guardamos
    #en la tabla de preguntas sin responder
        if str(frase in preguntas) == 'False': #Verificamos la nueva pregunta sin
        #responder no esté ya guardada, para no realizar duplicados 

            try:
                sql = """
                      INSERT INTO preguntas(
                      pregunta
                      )
                      VALUES(?)
                      ;
                      """ #sql para insertar la pregunta
                cursor.execute(sql, (frase,)) #Ejecutamos la consulta
                conexion.commit() #Si todo fue bien hasta ahora, guardamos
                #los cambios en la bd
            except Exception as e: #Si ocurrió un error lo notificamos
                print("Hubo un problema al almacenar la pregunta. \nError: " + str(e)) 
                print(frase)             

        print("Entonces cambiemos de tema, cuando sepas la respuesta me enseñas")
        engine.say("Entonces cambiemos de tema, cuando sepas la respuesta me enseñas")
        engine.runAndWait()
        
        
        if len_preguntas > 0: 
            hay_preguntas_para_hacer = True
        else:
            hay_preguntas_para_hacer = False                

        resta = int(datetime.datetime.now().strftime("%M")) - int(hora_de_inicio) #Obte-
        #nemos la resta entre la hora de inicio y la hora actual

        if resta > 4 or resta < 0 and hay_preguntas_para_hacer == True: #Si la
        #resta da como resultado un número mayor a 4, significa que han transcurrido
        #5 minutos o más, y si la resta es menor a 0 (número negativo), entonces
        #significa que han transcurrido 5 minutos o inclusive más. Por último
        #verificamos que existan preguntas para hacer.
               
            pregunta_escogida = random.choice(preguntas) #Escogemos aleatoriamente 
            #una pregunta para preguntar si ya se sabe la respuesta
            

            print("A proposito, ¿Ya sabes cómo responder a esta conversación?")
            print("\n \"", pregunta_escogida,"\"")
            engine.say("A propósito, ¿Ya sabes cómo responder a esta conversación?")
            engine.runAndWait()
            aux = input('Si = S \nNo = Cualquier caracter\n-->')

            if str(aux) == 'S' or str(aux) == 's': #Si dicen que si saben la respuesta
                print("Entonces digita a continuación cómo responder a: ", pregunta_escogida)
                engine.say("Entonces digita a continuación cómo responder a")
                engine.runAndWait() 
                respuesta = input('Respuesta: ')
                try: 
                    sql = """
                          DELETE FROM preguntas 
                          WHERE pregunta = ?
                          ;
                          """ #sql para eliminar la pregunta de la 
                          #tabla de preguntas por responder
                    cursor.execute(sql, (pregunta_escogida,)) #Ejecutamos
                    #la consulta  
                    
                    sql = """
                          INSERT INTO conversaciones(
                          frase, 
                          respuesta
                          )
                          VALUES(?, ?)
                          ;
                          """ #sql para insertar la nueva conversación
                    cursor.execute(sql, (pregunta_escogida, respuesta)) #Ejecutamos
                    #la consulta
                 
                    trainer.train([ 
                    str(pregunta_escogida),
                    str(respuesta)
                    ]) #Si todo fue bien entrenamos al bot

                    conexion.commit() #Si todo fue bien, guardamos
                    #los cambios en la bd

                    print("Conversación aprendida exitosamente")
                    engine.say("Conversación aprendida exitosamente")    
                    engine.runAndWait()
                    
                except Exception as e: #Si hubo un error lo notificamos
                    print("Hubo un problema al entrenar el bot. \nError: " + str(e))


                hora_de_inicio = datetime.datetime.now().strftime("%M") #La hora 
                #actual será la nueva hora de inicio
                cursor.close() #Cerramos la conexión con el cursor
                conexion.close() #Cerramos la conexión a la bd
                return hora_de_inicio

            else: #Si no sabe la respuesta
                print("Ok, será en otra ocasión")
                engine.say("Ok, será en otra ocasión")
                engine.runAndWait()   
                cursor.close() #Cerramos la conexión con el cursor
                conexion.close() #Cerramos la conexión a la bd
                return hora_de_inicio 

    cursor.close() #Cerramos la conexión con el cursor
    conexion.close() #Cerramos la conexión a la bd
    return hora_de_inicio        

#Proyecto Final - Inteligencia Artficial II
#Integrantes:
#Rodriguez Uresti Francisco Maximiliano - 170882
#Ramirez Castillo Daniela Guadalupe - 170659
#Arenas Loredo Erick David - 171270

#Se importan las librerias necesarias para ejecutar el código
import tkinter as tk
from tkinter import filedialog
from tkinter import Entry
from turtle import exitonclick
from fpdf import fpdf
import pdfkit
import os
import random
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
# Se utiliza sentence_splitter para dividir el texto en oraciones
from sentence_splitter import SentenceSplitter
splitter = SentenceSplitter(language = 'es')


def cerrar():       #Funcion para cerrar la ventana
    window.quit()


def browseFiles():  #Funcion para mostrar el explorador de archivos
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    #Cambia el contenido del label del buscador de archivos
    label_file_explorer.configure(text="File Opened: ")
    entry.insert(0, filename)   


def button_event1():
    try:
        texto = entry.get() #Se obtiene la ruta como string
        porcentaje= int(entry2.get())   #Se obtiene el porcentaje de la text box como entero
        #Abrimos el archivo ingresado por el usuario
        with open(texto,"r",encoding="utf8") as entrada:
            texto_split=entrada.read()
        #Definimos el corpus que en este caso es el conjunto de las oraciones
        corpus=splitter.split(texto_split) 
        #Definimos el arreglo siguiente a utilizar en base al porcentaje
        corpus2=[None]*len(corpus)
        #Calculamos el tamaño del array
        tam=len(corpus)
        #Realizamos la regla de 3 para poder solo utilizar la cantidad 
        #correspondiente al porcentaje de oraciones
        y=(porcentaje*tam)/100
        #Redondeamos el numero a entero
        no_oraciones=int(y)
        #Ciclo For para utilizar nuevo corpus en base al porcentaje/numero
        for i in range(no_oraciones):
           corpus2[i]=corpus[i]
        # using naive method
        # to remove None values in list
        res = []    #Inicializamos nuestro vector a almacenar las oraciones
        for val in corpus2: #Por cada valor en el corpus2
            if val != None :        #Si no es None
                res.append(val)         #Lo almacena en el array res
  
        #Se vectoriza el resultado (res) 
        vectorizer=TfidfVectorizer()
        X= vectorizer.fit_transform(res)
        #Vocabulario realizado en base al resultado (res)
        vocabulario= vectorizer.get_feature_names_out()
        #matriz vectorizada del resultado (res)
        matriz_tfidf=vectorizer.fit_transform(res)
        tabla_tfidf=pd.DataFrame(matriz_tfidf.toarray(),index=res,columns=vocabulario)
        #Se toma la suma de cada fila para conocer el valor de importancia de la sentencia
        resultado=tabla_tfidf.sum(axis=1, numeric_only=float)
        #Se toman unicamente las 2 oraciones con mas importancia, es decir, que tengan el mayor valor
        resultado=resultado.nlargest(2)
        #Se imprime el resumen terminado
        resumen=resultado.index.format()
        #Inicializamos la nueva instancia fpdf para poder guardar el resumen como pdf
        pdf = fpdf.FPDF(format='letter')
        pdf.set_font("Arial", size=12)
        pdf.add_page()  #Añadimos una nueva pagina
        for i in resumen:   #Por cada posicion en el arreglo del resumen
          pdf.write(5,str(i))   #Imprime
          pdf.ln()          #Salta linea
        pdf.output("Resumen.pdf")  #Lo guarda con el nombre
        #Muestra el resumen en la text box
        text_box.insert("1.0",resumen)

    except:
        label6 = tk.Label(text="Ingresa una ruta/numero de oraciones valido")       #Si no introduce la ruta/numero de oraciones valido
        label6.pack()
        entry.delete(0, tk.END)     #Vuelve a borrar los datos
        entry2.delete(0, tk.END)    #Vuelve a borrar los datos

window = tk.Tk()    #Inicializamos una nueva instancia del Tinkert
window.title("Proyecto Final - Inteligencia Artficial 2")   #Titulo de la ventana
window.geometry("750x750")  #Tamaño de la ventana

label = tk.Label(text="Aplicacion de Creacion de Resumenes - Inteligencia Artificial II - Proyecto Final") 
label.pack()
label_file_explorer = tk.Label(text = "Explorador de Archivos")
label_file_explorer.pack()
button_explore = tk.Button(text = "Buscar Archivo",font=("Calibri",12,"bold"),command = browseFiles)    #Invoca al evento de busqueda de archivos
button_explore.pack()
entry = tk.Entry(fg="yellow", bg="black")   #Entrada donde se pone la ruta del archivo txt
entry.pack()
label3 = tk.Label(text="Ingresa el porcentaje de oraciones a trabajar (10-100%): ")  #Numero de oraciones que sea igual o menor a las oraciones del texto
label3.pack()
entry2 = tk.Entry(fg="yellow", bg="black")
entry2.pack()
button = tk.Button(text="Resumir Texto",font=("Calibri",12,"bold"),command=button_event1)      #Evento del boton que realiza el resumen
button.pack()
text_box = tk.Text()
text_box.pack()
button_exit=tk.Button(text= "Salir", font=("Calibri",12,"bold"), command=cerrar)        #Evento del boton que finaliza la sesion
button_exit.pack()

window.mainloop()       #Mantiene la ventana en funcionamiento como principal

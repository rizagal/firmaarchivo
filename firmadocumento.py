import PIL.Image
from tkinter import *
from tkinter import messagebox as Messagebox
import io
import os
import datetime
from getpass import getuser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


##El siguiente archivo json se descarga de firebase y se debe colocar en la misma carpeta del aplicativo
cred = credentials.Certificate('Llave de firebase')
firebase_admin.initialize_app(cred)
db = firestore.client()

clave = 'wdmurcielagokptvhfs'
codigo=list(clave)
def encriptar(f):
  salida=''
  for i in f:
    if i in clave:
      salida+=str(codigo.index(i))
    else:
      salida+=i
  return(salida)


def desencriptar(f):
  texto=''
  for i in f:
    if i.isdigit():
      texto+=codigo[int(i)]
    else:
      texto+=i
  return(texto)


def firmar():
#Escribir un texto en el archivo
#Verificar si el documento existe en la ruta donde esta este archivo ejecutable
  if  os.path.exists(nombre_archivo.get()):
    #Siempre comenzar el archivo por XYZ para poder que el codigo hexadecimal buscado se uno solo el cual es 58595A
    with open(nombre_archivo.get(), 'ab') as f:
        verifica_firmante = encriptar("b'XYZ " + str(getuser()) + "'")
        print(encriptar(verifica_firmante))        
        f.write(verifica_firmante.encode())    
        Messagebox.showinfo("Firmar Documento","Se Firmo Documento")    
        hora_actual = str(datetime.datetime.now()).replace(" ", "")
        doc_ref = db.collection(u'firma_documentos').document(hora_actual[0:15])
        doc_ref.set({
                    u'nombre_quienfirma': str(getuser()),
                    u'hora': str(datetime.datetime.now()),
                    u'nombre_documento': nombre_archivo.get()
                    })
        

#Leer texto oculto en el archivo
def verificafirma():
    with open(nombre_archivo.get(), 'rb') as f:
        content = f.read()
        offset = content.index(bytes.fromhex('58595A'))
        f.seek(offset + 4) 
        #Entre la anterior linea y la siguiente no puede haber codigo alguno porque se pierde el valor de f.read
        if getuser() in desencriptar(str(f.read())) :
            Messagebox.showinfo("Verifica Firma","Esta Firmado por el Usuario Logueado")
        else:
            Messagebox.showwarning("Verifica Firma","No esta Firmado")


#Leer texto oculto en el archivo
def usuariofirma():
    with open(nombre_archivo.get(), 'rb') as f:
        content = f.read()
        offset = content.index(bytes.fromhex('58595A'))
        f.seek(offset + 4) 
        #Entre la anterior linea y la siguiente no puede haber codigo alguno porque se pierde el valor de f.read
        Messagebox.showinfo("Verifica Firma", desencriptar(str(f.read())))
       
      
root = Tk()
root.resizable(0,0)
root.config(bd=30)
root.title("Firmar Documento")

imagen = PhotoImage(file="firma.png")
foto = Label(root, image=imagen, bd=0)
foto.grid(row=0, column=0, rowspan=2)

menubar = Menu(root)
root.config(menu=menubar)
helpmenu = Menu(menubar, tearoff=0)


menubar.add_command(label="Firmar Documento", command=firmar)
menubar.add_command(label="Verificar Firma con Usuario Windows", command=verificafirma)
menubar.add_command(label="Usuario que Firmo", command=usuariofirma)
menubar.add_command(label="Salir", command=root.destroy)


instrucciones = Label(root, text="Nombre del Documento\n")
instrucciones.grid(row=0,column=1,  sticky="s")

nombre_archivo = Entry(root)
nombre_archivo.grid(row=1, column=1, sticky="n")


root.mainloop()#Esta linea es importante para que se muestre el contenido de la ventana





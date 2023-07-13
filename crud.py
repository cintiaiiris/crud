import sqlite3 as sq3
from tkinter import *
from tkinter import messagebox # ventanas emergentes 
import matplotlib.pyplot as plt  # modulo spoilet del crud, sirve para hacer graficos


'''
ENTORNOS VIRTUALES
1ra vez: INSTALACION de virtualenv
pip install virtualenv

CREAR ENTORNO VIRTUAL
virtualenv {nombre}

ACTIVAR EL ENTORNO VIRTUAL
{nombre\Scripts\activate}

VER QUE HAY INSTALADO EN EL ENTORNO ACTUAL
pip list

INSTALAR LIBRERIAS
pip install{nombre_libreria}

DISTRIBUCION
- Grabar requerimientos del entorno virtual
pip freeze > requeriments.txt
- Crear un entorno vitual para instalar los requerimientos
pip install -r requeriments.txt 

DESACTIVAR EL ENTORNO VIRTUAL
deactivate
--------------------------------------
DOCUMENTACIÓN: https://virtualenv.pypa.io/en/stable/index.html 
'''

''' 
*******************
PARTE FUNCIONAL
*******************
'''
# MENU BBDD -  Conecta a la BBDD
def conectar():
    global con #para que el CON y CUR este disponible en todas partes los convierto en GLOBAL
    global cur
    con = sq3.connect('mi_db.db') #conexion
    cur = con.cursor() #cursor
    # necesito un mensaje inicial, informativo uso el MESSAGEBOX
    messagebox.showinfo('STATUS', 'Conectado a la BBDD!!')
    # activar el boton, conectar con la funcion
    
# Menu BBDD - Listar
def listar():
    class Table():
        def __init__(self, raiz2):
            nombre_cols = ['Legajo', 'Apellido','Nombre','Promedio','Email','Escuela','Localidad','Provincia']
            for i in range(cant_cols):
                self.e = Entry(frameppal)
                self.e.config(bg='black',fg='white')
                self.e.grid(row=0, column=i)
                self.e.insert(END,nombre_cols[i])
                
            for fila in range(cant_filas):
                for col in range(cant_cols):
                    self.e = Entry(frameppal)                    
                    self.e.grid(row=fila+1, column=col)
                    self.e.insert(END,resultado[fila][col])
                    self.e.config(state='readonly')    
                
                
    raiz2 = Tk()
    raiz2.title('Listado de alumnos')
    frameppal = Frame(raiz2)
    frameppal.pack(fill = 'both')
    framecerrar = Frame(raiz2)
    framecerrar.config(bg=color_fondo)
    framecerrar.pack(fill='both')
    boton_cerrar = Button(framecerrar, text='CERRAR', command=raiz2.destroy)
    boton_cerrar.config(bg=color_fondo_boton, fg=color_letra_boton, pady=10, padx=10)
    boton_cerrar.pack(fill='both')
    
    # obtengo los datos -> Messi el query1 del ejemplo de sqlite
    con = sq3.connect('mi_db.db')
    cur = con.cursor()
    query1 = "SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id LIMIT 5"
    cur.execute(query1)
    resultado = cur.fetchall()
    # [(), (), (),()]
    cant_filas = len(resultado)
    cant_cols = len(resultado[0])
    
    tabla = Table(frameppal)
    con.close()
    raiz2.mainloop()
    
    
# MENU BBDD - Salir 
def salir():
    resp = messagebox.askquestion('CONFIRME','Desea salir de la aplicacion??')
    if resp == 'yes':
        con.close()
        raiz.destroy() # destruir la interfaz grafica
    # asocio el boton con la funcion salir
    
# MENU Limpiar
def limpiar():
    legajo.set("") # el metodo SET le pone un valor, en este caso quiero que el valor sea una cadena vacia
    apellido.set("")
    nombre.set("")
    email.set("")
    calificacion.set("")
    escuela.set("Seleccione")
    localidad.set("")
    provincia.set("")
    legajo_input.config(state='normal') # los estado son solo lectura, normal y desabilitado
    # Habilitar el boton limpiar    
    
    # MENU ACERCA DE...
def mostrar_licencia():
        # CREATIVE COMMONS GNU GPL https://www.gnu.org/licenses/gpl-3.0.txt (textos genericos sobre las licencias)
        msg = ''' 
        Sistema CRUD en Python
        Copyright (C) 2023 - xxxxx xxxx
        Email: xxxx@xxx.xx\n=======================================
        This program is free software: you can redistribute it 
        and/or modify it under the terms of the GNU General Public 
        License as published by the Free Software Foundation, 
        either version 3 of the License, or (at your option) any 
        later version.
        This program is distributed in the hope that it will be 
        useful, but WITHOUT ANY WARRANTY; without even the 
        implied warranty of MERCHANTABILITY or FITNESS FOR A 
        PARTICULAR PURPOSE.  See the GNU General Public License 
        for more details.
        You should have received a copy of the GNU General Public 
        License along with this program.  
        If not, see <https://www.gnu.org/licenses/>. '''
        messagebox.showinfo('LICENCIA', msg)
        
def mostrar_acercade():
    messagebox.showinfo('ACERCA DE...','Creado por Regina N. Molares\npara Codo a Codo 4.0 - Big Data\nMayo, 2022\nEmail: regina.molares@bue.edu.ar')
    
    
# FUNCIONES CRUD
# crear
def crear():
    id_escuela = int(buscar_escuelas(True)[0])
    datos = id_escuela, legajo.get(), apellido.get(), nombre.get(), calificacion.get(), email.get()
    cur.excute('INSERT INTO alumnos (id_escuela, legajo, apellido, nombre, nota, email) VALUES (?,?,?,?,?,?)', datos) # nombre de las columnas y sus datos??????
    con.commit()
    messagebox.showinfo('STATUS', 'Registro agregado')
    limpiar()
    
# buscar
def buscar_legajo():
    query_buscar = '''SELECT alumnos.legajo, alumnos.apellido, alumnos.nombre, alumnos.nota, alumnos.email, escuela.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id WHERE alumnos.legajo='''
    cur.execute(query_buscar + legajo.get())
    resultado = cur.fetchall()
    if resultado == []:
        messagebox.showerror('EROR', 'Ese No de legajo no existe')
        legajo.set("")
    else:
        for campo in resultado:
            legajo.set(campo[0])
            apellido.set(campo[1])
            nombre.set(campo[2])
            calificacion.set(campo[3])
            email.set(campo[4])
            escuela.set(campo[5])
            localidad.set(campo[6])
            provincia.set(campo[7])
            legajo_input.config(state='disabled')
    

# actualizar
def actualizar():
     id_escuela = int(buscar_escuelas(True)[0])
     datos = id_escuela, apellido.get(), nombre.get(), calificacion.get(), email.get()
     cur.execute('UPDATE alumnos SET id_escuelas=?, apellido=?, nombre=?, nota=?, email=? WHERE legajo=' + legajo.get(), datos)
     con.commit()
     messagebox.showinfo('STATUS', 'Registro actualizado')
     limpiar()   

# borrar
def borrar():
    resp = messagebox.askquestion('CONFIRME', 'Desea eliminar el registro?')
    if resp == 'yes':
        cur.excute('DELETE FROM alumnos WHERE legajo =' + legajo.get())
        con.commit()
        messagebox.showinfo('STATUS', 'Registro eliminado')
        limpiar()

# FUNCIONES VARIAS
def buscar_escuelas(actualiza):
    con = sq3.connect('mi_db.db') #conexion
    cur = con.cursor() #cursor 
    if actualiza:
        cur.execute('SELECT _id, localidad, provincia FROM escuelas WHERE nombre =?', (escuela.get(),)) # no olvidar la coma para que sea una TUPLA
    else: # esta opcion solo llena la lista de escuelas en OptionMenu
         cur.execute('SELECT nombre FROM escuelas')
         
    resultado = cur.fetchall() # RECIBO UNA LISTA DE TUPLAS con un elemento "fantasma"
    # [(),(),(),()] ---> tupla = (5,6,7,8,9) / tupla = 5,6,7,8,9
    # ["a", "b", "c", "d"] -----> [("a",), ("b",),("c",),("d",)] una lista de tuplas para no confundir si es una tupla o es una lista
    retorno = []
    for e in resultado:
        if actualiza:
            localidad.set(e[1]) # indice 1, provincia indice 2
            provincia.set(e[2])
        esc = e[0]
        retorno.append(esc)
    con.close()
    return retorno

# GRAFICAS
# Por Escuelas
def alumnos_x_escuelas():
    query_buscar = ''' SELECT COUNT(alumnos.legajo) AS "total", escuelas.nombre FROM  alumnos INNER JOIN escuelas ON alumnos.id_escuela=escuelas._id GROUP BY escuelas.nombre ORDER BY total DESC'''
    cur.execute(query_buscar)
    resultado = cur.fetchall()
    # print(resultado)

    cuenta=[]
    n_escuela = []
    for i in resultado:
        cuenta.append(i[0])
        n_escuela.append(i[i])
        
    plt.bar(n_escuela, cuenta) #genero la grafica
    plt.xticks(rotation = 90) # roto los labels de las escuelas 
    plt.show() # muestra la grafica
    
# Por nota
def alumnos_x_notas():
    query_buscar = ''' SELECT COUNT(legajo) AS "total", nota FROM  alumnos GROUP BY nota ORDER BY total DESC''' # La recta de valores continuos mata el order by
    cur.execute(query_buscar)
    resultado = cur.fetchall()
    # print(resultado)

    cuenta=[]
    nota = []
    for i in resultado:
        cuenta.append(i[0])
        nota.append(i[i])
        
    plt.bar(nota, cuenta) #genero la grafica
    plt.xticks(rotation = 90) # roto los labels de las escuelas 
    plt.show() # muestra la grafica

    
'''
*******************
INTERFAZ GRAFICA
*******************
'''

# colores de framecampos
color_fondo = 'cyan'
color_letra = 'black'
# colores de framebotones
fondo_framebotones = 'plum'
color_fondo_boton = 'black'
color_letra_boton = fondo_framebotones

# Raiz
raiz = Tk()
raiz.title('Ejemplo de Interfaz Grafica')

# Barra menu
barramenu = Menu(raiz)
raiz.config(menu=barramenu) # **kwargs

# Menu BBDD
bbddmenu = Menu(barramenu, tearoff=False)
bbddmenu.add_command(label = 'conectar a la BBDD', command=conectar)  # activar el boton, conectar con la funcion
bbddmenu.add_command(label = 'Mostrar listado de alumnos', commamd=listar)
bbddmenu.add_command(label = 'salir', command=salir)     # asocio el boton con la funcion salir


# Menu Graficas
estadmenu = Menu(barramenu, tearoff=0)
estadmenu.add_command(label = 'Alumnos por escuela', command=alumnos_x_escuelas)
estadmenu.add_command(label = 'Calificaciones', command = alumnos_x_notas)

# Menu Limpiar
limpiarmenu = Menu(barramenu, tearoff=0)
limpiarmenu.add_command(label  = 'Limpiar Campos', command=limpiar)     # Habilitar el boton limpiar    con command


# Menu Acerca de....
ayudamenu = Menu(barramenu, tearoff=0)
ayudamenu.add_command(label='Licencia', command=mostrar_licencia)
ayudamenu.add_command(label='Acerca de...', command=mostrar_acercade)

barramenu.add_cascade(label =  'BBDD', menu = bbddmenu)
barramenu.add_cascade(label =  'Graficas', menu = estadmenu)
barramenu.add_cascade(label =  'Limpiar', menu = limpiarmenu)
barramenu.add_cascade(label =  'Acerca de...', menu = ayudamenu)

# ------FRAMECAMPOS-------
framecampos = Frame(raiz) # ubicacion, dentro del contenedor raiz
framecampos.pack(fill='both') # la dimension del campo para que use a lo largo y a lo ancho
framecampos.config(bg=color_fondo) #aplico los colores

# Labels
'''
"STICKY"
     n
  nw   ne
w         e
  sw   se
     s
'''

# Labels/ se pueden configurar todos los elementos con una funcion
def config_label(mi_label, fila):
    espaciado_labels= {'column':0, 'sticky':'e', 'padx':10, 'pady':10}
    color_label = {'bg':color_fondo, 'fg': color_letra}
    mi_label.grid(row=fila, **espaciado_labels)
    mi_label.config(**color_label)
    
legajo_label = Label(framecampos, text='Nro de Legajo')
config_label(legajo_label, 0)
# legajo_label.config(bg=color_fondo, fg=color_letra) # colores de la etiqueta
# legajo_label.grid(row=0,column=0, padx=10, pady=10, sticky='e') # Ubicacion(metodo GRID), ubicacion de la etique en la grilla, (padx =espaciado horizontal)(pady=espaciado vertical), justificado a la derecha(atributo sticky- puntos cardinales)

apellido_label = Label(framecampos, text='Apellido')
config_label(apellido_label, 1)

nombre_label = Label(framecampos, text='Nombre')
config_label(nombre_label, 2)

email_label = Label(framecampos, text='Email')
config_label(email_label, 3)

calificacion_label = Label(framecampos, text='Promedio')
config_label(calificacion_label, 4)

escuela_label = Label(framecampos, text='Escuela')
config_label(escuela_label, 5)

localidad_label = Label(framecampos, text='Localidad')
config_label(localidad_label, 6)

provincia_label = Label(framecampos, text='Provincia')
config_label(provincia_label, 7)

# ENTRY
'''
entero = IntVar()  # Declara variable de tipo entera
flotante = DoubleVar()  # Declara variable de tipo flotante
cadena = StringVar()  # Declara variable de tipo cadena
booleano = BooleanVar()  # Declara variable de tipo booleana
'''
# Crear variables de control para los campos de entrada
legajo = StringVar()
apellido = StringVar()
nombre = StringVar()
email = StringVar()
calificacion = DoubleVar()
escuela = StringVar()
localidad = StringVar()
provincia = StringVar()

def config_input(mi_input, fila):
    espaciado_input ={'column':1, 'padx':10, 'pady': 10, 'ipadx':50}
    mi_input.grid(row=fila, **espaciado_input)
    
legajo_input = Entry(framecampos, textvariable=legajo)
config_input(legajo_input, 0)

apellido_input = Entry(framecampos, textvariable=apellido)
config_input(apellido_input, 1)

nombre_input = Entry(framecampos, textvariable=nombre)
config_input(nombre_input, 2)

email_input = Entry(framecampos, textvariable=email)
config_input(email_input, 3)

calificacion_input = Entry(framecampos, textvariable=calificacion)
config_input(calificacion_input, 4)

# volara
# escuela_input = Entry(framecampos, textvariable=escuela)  # lista desplegable
# config_input(escuela_input, 5)
n_escuelas = buscar_escuelas(False) # nombre de la escuelas en una LISTA
escuela.set("Seleccione") # setear la variable
escuela_option = OptionMenu(framecampos, escuela, *n_escuelas) # *n_escuelas el astericos es para que los datos esten desplegados y no uno al lado de otro
escuela_option.grid(row=5, column=1,padx=10,pady=10,ipadx=50,sticky='w')

localidad_input = Entry(framecampos, textvariable=localidad)
config_input(localidad_input, 6)
localidad_input.config(state='readonly')

provincia_input = Entry(framecampos, textvariable=provincia)
config_input(provincia_input, 7)
provincia_input.config(state='readonly')

# FrameBotones
framebotones = Frame(raiz) # creo el objeto
framebotones.pack(fill='both')
framebotones.config(bg=fondo_framebotones)

def config_buttons(mi_button, columna):
    espaciado_buttons = {'row': 0, 'padx':5, 'pady':10, 'ipadx':12 }
    mi_button.config(bg=color_fondo_boton, fg=color_letra_boton)
    mi_button.grid(column=columna, **espaciado_buttons)
    
boton_crear =Button(framebotones, text='Crear', command = crear)
config_buttons(boton_crear, 0)

boton_buscar =Button(framebotones, text='Buscar', command=buscar_legajo)
config_buttons(boton_buscar, 1)

boton_actualizar =Button(framebotones, text='Actualizar', command=actualizar)
config_buttons(boton_actualizar, 2)

boton_borrar =Button(framebotones, text='Eliminar', command=borrar)
config_buttons(boton_borrar, 3)

# Frame del Pie
framecopy = Frame(raiz)
framecopy.config(bg='black')
framecopy.pack(fill='both')

copylabel = Label(framecopy, text= '(2023) por Regina N Molares para CaC 4.0 - Big Data')
copylabel.grid(row=0, column=0, padx=13, pady=10)
copylabel.config(bg='black', fg='white')

raiz.mainloop()
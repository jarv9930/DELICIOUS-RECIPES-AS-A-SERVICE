from tkinter import *
from tkinter import filedialog
root = Tk()

root.title("Aplicacion Chef")

def AsignarAcuerdo():
    DireccionArchivo = filedialog.askopenfile()




Inicio = Frame(root)
#Inicio.pack()

BotonCambiarAcuerdo = Button(Inicio,text="Cambiar acuerdo",command=)
BotonCambiarAcuerdo.grid(row=0,column=0)
BotonIngresarReceta = Button(Inicio,text="Ingresar nueva receta",command=)
BotonIngresarReceta.grid(row=1,column=0)

Recetas = Frame(root)
#Recetas.pack()

BotonCambiarAcuerdo = Button(Recetas,text="Cambiar acuerdo",command=)
BotonCambiarAcuerdo.grid(row=0,column=0)
BotonIngresarReceta = Button(Recetas,text="Ingresar nueva receta",command=)
BotonIngresarReceta.grid(row=1,column=0)

Acuerdo = Frame(root)

#Acuerdo.pack()
Acuerdo.config(width="400",height="400")



Label1 = Label(Acuerdo,text="Ingresa un acuerdo de confidencialidad")
Label1.grid(row=0,column=0)

BotonAsignar = Button(Acuerdo,text= "Escoger archivo",command= AsignarAcuerdo)
BotonAsignar.grid(row=1,column=0)

#Acuerdo.destroy()

root.mainloop()


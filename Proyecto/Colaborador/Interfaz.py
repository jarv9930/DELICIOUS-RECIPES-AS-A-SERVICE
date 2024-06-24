from tkinter import *
from tkinter import filedialog
root = Tk()

root.title("Aplicacion Colaborador")

def AsignarAcuerdo():
    print("hol")




Inicio = Frame(root)
#Inicio.pack()

#BotonCambiarAcuerdo = Button(Inicio,text="Cambiar acuerdo",command=)
#BotonCambiarAcuerdo.grid(row=0,column=0)
#BotonIngresarReceta = Button(Inicio,text="Ingresar nueva receta",command=)
#BotonIngresarReceta.grid(row=1,column=0)

Recetas = Frame(root)
#Recetas.pack()



Acuerdo = Frame(root)

Acuerdo.pack()
Acuerdo.config(width="400",height="400")



LabelAcuerdo = Label(Acuerdo,text="Lea el siguiente acuerdo de confidencialidad antes de aceptarlo para poder obtener acceso:")
LabelAcuerdo.grid(row=0,column=0)


Acuerdo = Entry(Acuerdo)
Acuerdo.grid(row=1,column=0)


BotonAcceptar = Button(Acuerdo,text= "Aceptar",command= AsignarAcuerdo)
BotonAcceptar.grid(row=2,column=0)

BotonRechazar = Button(Acuerdo,text= "Rechazar",command= AsignarAcuerdo)
BotonRechazar.grid(row=2,column=1)

#Acuerdo.destroy()

root.mainloop()


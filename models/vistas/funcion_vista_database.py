from ..controllers.personal_controller import PersonalController
from sqlite3 import Error
from tkinter import *
from tkinter import messagebox

class PersonalVista():

    def __init__(self):
        self.controller= PersonalController()
        self.root= Tk()

        self.cedula= StringVar()
        self.primer_nombre= StringVar()
        self.segundo_nombre= StringVar()
        self.primer_apellido= StringVar()
        self.segundo_apellido= StringVar()
        self.telefono= StringVar()
        self.nombre_usuario= StringVar()
        self.password= StringVar()

        self.crear_interfaz()
        self.root.mainloop()

    def crear_interfaz(self):

        # Creación del frame del formulario
        form= Frame(self.root)
        form.pack()
        self.root.title("Registrar Personal")

        # Labels del formulario
        labelCedula= Label(form, text="Cedula:").grid(row=0, column=0, sticky="e", padx= 10, pady= 10)
        labelPrimerNombre= Label(form, text="Primer nombre:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        labelSegundoNombre= Label(form, text="Segundo nombre:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        labelPrimerApellido= Label(form, text="Primer apellido:").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        labelSegundoApellido= Label(form, text="Segundo apellido:").grid(row=4, column=0, sticky="e", padx=10, pady=10)
        labelTelefono= Label(form, text="Teléfono:").grid(row=5, column=0, sticky="e", padx=10, pady=10)
        labelNombreUsuario= Label(form, text="Username:").grid(row=6, column=0, sticky="e", padx=10, pady=10)
        labelPassword= Label(form, text="Password:").grid(row=7, column=0, sticky="e", padx=10, pady=10)

        # Entrys del formulario
        entryCedula= Entry(form, textvariable=self.cedula).grid(row=0, column=1, padx= 10, pady= 10)
        entryPrimerNombre= Entry(form, textvariable=self.primer_nombre).grid(row=1, column=1, padx= 10, pady= 10)
        entrySegundoNombre= Entry(form, textvariable=self.segundo_nombre).grid(row=2, column=1, padx= 10, pady= 10)
        entryPrimerApellido= Entry(form, textvariable=self.primer_apellido).grid(row=3, column=1, padx= 10, pady= 10)
        entrySegundoApellido= Entry(form, textvariable=self.segundo_apellido).grid(row=4, column=1, padx= 10, pady= 10)
        entryTelefono= Entry(form, textvariable=self.telefono).grid(row=5, column=1, padx= 10, pady= 10)
        entryNombreUsuario= Entry(form, textvariable=self.nombre_usuario).grid(row=6, column=1, padx= 10, pady= 10)
        entryPassword= Entry(form, textvariable=self.password).grid(row=7, column=1, padx= 10, pady= 10)

        # Creación del frame del CRUD
        crud= Frame(self.root)
        crud.pack()

        buttonCrear= Button(crud, text="Crear", padx= 10, pady= 10).grid(row=0, column=0, padx= 10, pady= 10)
        buttonLeer= Button(crud, text="Leer", padx= 10, pady= 10).grid(row=0, column=1, padx= 10, pady= 10)
        buttonActualizar= Button(crud, text="Actualizar", padx= 10, pady= 10).grid(row=0, column=2, padx= 10, pady= 10)
        buttonEliminar= Button(crud, text="Eliminar", padx= 10, pady= 10).grid(row=0, column=3, padx= 10, pady= 10)
        buttonLimpiar= Button(crud, text="Limpiar", padx= 10, pady= 10).grid(row=0, column=4, padx= 10, pady= 10)


# Para iniciar la aplicación
if __name__ == "__main__":
    vista = PersonalVista()

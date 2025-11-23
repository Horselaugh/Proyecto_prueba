import sys
import os
import customtkinter as ctk
from tkinter import messagebox

# Agregar el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# CORRECCIÓN CLAVE: PersonalVista debe heredar de ctk.CTkFrame
# y recibir el master (contenedor) y el controller inyectado
class PersonalVista(ctk.CTkFrame):
    
    # MODIFICACIÓN CLAVE: Recibir master y controller
    def __init__(self, master, controller=None):
        super().__init__(master, fg_color="transparent") # Inicializa como un frame
        
        # Configurar el frame principal (que es 'self')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Variables de control
        self.cedula = ctk.StringVar(self)
        self.primer_nombre = ctk.StringVar(self)
        self.segundo_nombre = ctk.StringVar(self)
        self.primer_apellido = ctk.StringVar(self)
        self.segundo_apellido = ctk.StringVar(self)
        self.telefono = ctk.StringVar(self)
        self.nombre_usuario = ctk.StringVar(self)
        self.password = ctk.StringVar(self)

        self.crear_interfaz()
        # Se elimina self.root.mainloop()

    def crear_interfaz(self):
        # Frame de Contenido Scrollable
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#3c3c3c", corner_radius=10, label_text="👥 Registro de Nuevo Personal")
        scroll_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        scroll_frame.columnconfigure(1, weight=1) # Columna de entradas es flexible

        # Título
        ctk.CTkLabel(scroll_frame, text="Registro de Personal", 
                     font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="n")

        # Campos del Formulario
        fields = [
            ("Cédula", self.cedula),
            ("Primer Nombre", self.primer_nombre),
            ("Segundo Nombre", self.segundo_nombre),
            ("Primer Apellido", self.primer_apellido),
            ("Segundo Apellido", self.segundo_apellido),
            ("Teléfono (11 dígitos)", self.telefono),
            ("Nombre de Usuario", self.nombre_usuario),
            ("Contraseña", self.password, True), # El tercer elemento indica si es campo de contraseña
        ]
        
        current_row = 1
        for label_text, var, *is_password in fields:
            is_pass = is_password[0] if is_password else False
            
            ctk.CTkLabel(scroll_frame, text=label_text, font=("Arial", 14)).grid(row=current_row, column=0, sticky="w", padx=20, pady=(10, 5))
            
            entry = ctk.CTkEntry(scroll_frame, textvariable=var, height=40, font=("Arial", 14), 
                                 show="*" if is_pass else "")
            entry.grid(row=current_row, column=1, sticky="ew", padx=20, pady=(10, 5))
            
            current_row += 1

        # Botón de Registro
        ctk.CTkButton(scroll_frame, text="✅ Registrar Personal", command=self.agregar_personal, height=50, 
                      fg_color="#2ecc71", hover_color="#27ae60", font=ctk.CTkFont(size=18, weight="bold")).grid(row=current_row, column=0, columnspan=2, pady=(30, 20), padx=20, sticky="ew")

        # Botón Limpiar
        ctk.CTkButton(scroll_frame, text="🧹 Limpiar Formulario", command=self.limpiar_formulario, height=40, 
                      fg_color="#95a5a6", hover_color="#7f8c8d", font=ctk.CTkFont(size=14)).grid(row=current_row + 1, column=0, columnspan=2, pady=(0, 20), padx=20, sticky="ew")


    def agregar_personal(self):
        """Valida y registra un nuevo personal."""
        cedula = self.cedula.get().strip()
        primer_nombre = self.primer_nombre.get().strip()
        segundo_nombre = self.segundo_nombre.get().strip()
        primer_apellido = self.primer_apellido.get().strip()
        segundo_apellido = self.segundo_apellido.get().strip()
        telefono = self.telefono.get().strip()
        nombre_usuario = self.nombre_usuario.get().strip()
        password = self.password.get() # No strip en password por si se permiten espacios

        # Validación
        if not cedula or not primer_nombre or not primer_apellido:
            messagebox.showerror("❌ Error", "Cédula, Primer Nombre y Primer Apellido son obligatorios.")
            return

        if not cedula.isdigit() or len(cedula) < 6:
            messagebox.showerror("❌ Error", "La cédula debe ser numérica y válida.")
            return

        if len(telefono) != 11 or not telefono.isdigit():
            messagebox.showerror("❌ Error", "El teléfono debe tener exactamente 11 dígitos")
            return

        if not nombre_usuario or not password:
            messagebox.showerror("❌ Error", "Nombre de usuario y contraseña son obligatorios")
            return

        try:
            # Usar el controlador para agregar el personal
            persona_id = self.controller.agregar_personal(
                cedula, primer_nombre, segundo_nombre, primer_apellido, 
                segundo_apellido, telefono, nombre_usuario, password
            )
            if persona_id:
                messagebox.showinfo("✅ Éxito", f"👤 Personal registrado correctamente.\n\n🆔 ID asignado: {persona_id}\n👤 Usuario: {nombre_usuario}")
                self.limpiar_formulario()
            else:
                messagebox.showerror("❌ Error", "No se pudo registrar el personal")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al registrar personal: {str(e)}")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.cedula.set("")
        self.primer_nombre.set("")
        self.segundo_nombre.set("")
        self.primer_apellido.set("")
        self.segundo_apellido.set("")
        self.telefono.set("")
        self.nombre_usuario.set("")
        self.password.set("")

# Para iniciar la aplicación
# Se elimina el bloque if __name__ == '__main__':
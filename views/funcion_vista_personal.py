import customtkinter as ctk
from tkinter import messagebox
from models.personal_model import PersonalModel
from controllers.personal_controller import PersonalController

class PersonalVista():
    def __init__(self):
        self.model = PersonalModel()
        self.root = ctk.CTk()
        
        # Configurar ventana principal
        self.root.title("👥 Gestión de Personal - CPNNA Carrizal")
        self.root.geometry("1000x800")
        self.root.configure(fg_color="#2e2e2e")
        
        # Variables de control
        self.cedula = ctk.StringVar()
        self.primer_nombre = ctk.StringVar()
        self.segundo_nombre = ctk.StringVar()
        self.primer_apellido = ctk.StringVar()
        self.segundo_apellido = ctk.StringVar()
        self.telefono = ctk.StringVar()
        self.nombre_usuario = ctk.StringVar()
        self.password = ctk.StringVar()

        self.crear_interfaz()
        self.root.mainloop()

    def crear_interfaz(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="👥 REGISTRO DE PERSONAL",
            font=("Arial", 28, "bold"),
            text_color="#3498db"
        )
        title_label.pack(pady=(0, 30))

        # Frame del formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Configurar grid del formulario
        form_frame.columnconfigure(1, weight=1)

        # Campos del formulario con emojis
        campos = [
            ("🆔 Cédula*:", self.cedula, "Ej: V-12345678"),
            ("👤 Primer nombre*:", self.primer_nombre, "Ej: María"),
            ("👤 Segundo nombre:", self.segundo_nombre, "Ej: José"),
            ("👤 Primer apellido*:", self.primer_apellido, "Ej: González"),
            ("👤 Segundo apellido:", self.segundo_apellido, "Ej: Pérez"),
            ("📞 Teléfono*:", self.telefono, "11 dígitos - Ej: 04141234567"),
            ("👤 Nombre de usuario*:", self.nombre_usuario, "Ej: mgonzalez"),
            ("🔒 Contraseña*:", self.password, "Ingrese una contraseña segura")
        ]

        for i, (label, var, placeholder) in enumerate(campos):
            # Label
            ctk.CTkLabel(
                form_frame, 
                text=label, 
                font=("Arial", 14, "bold")
            ).grid(row=i, column=0, padx=20, pady=15, sticky="e")
            
            # Entry
            if "Contraseña" in label:
                entry = ctk.CTkEntry(
                    form_frame, 
                    textvariable=var,
                    placeholder_text=placeholder,
                    show="*",
                    height=45,
                    font=("Arial", 14)
                )
            else:
                entry = ctk.CTkEntry(
                    form_frame, 
                    textvariable=var,
                    placeholder_text=placeholder,
                    height=45,
                    font=("Arial", 14)
                )
            entry.grid(row=i, column=1, padx=20, pady=15, sticky="ew")

        # Frame de botones
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=30)

        # Botón Crear
        btn_crear = ctk.CTkButton(
            button_frame,
            text="💾 REGISTRAR PERSONAL",
            command=self.crear_personal,
            height=60,
            font=("Arial", 18, "bold"),
            fg_color="#27ae60",
            hover_color="#219a52"
        )
        btn_crear.pack(side="left", expand=True, padx=20)

        # Botón Limpiar
        btn_limpiar = ctk.CTkButton(
            button_frame,
            text="🧹 LIMPIAR FORMULARIO",
            command=self.limpiar_formulario,
            height=60,
            font=("Arial", 18, "bold"),
            fg_color="#f39c12",
            hover_color="#e67e22"
        )
        btn_limpiar.pack(side="right", expand=True, padx=20)

    def crear_personal(self):
        """Maneja la creación de nuevo personal"""
        datos = {
            "cedula": self.cedula.get(),
            "primer_nombre": self.primer_nombre.get(),
            "segundo_nombre": self.segundo_nombre.get(),
            "primer_apellido": self.primer_apellido.get(),
            "segundo_apellido": self.segundo_apellido.get(),
            "telefono": self.telefono.get(),
            "nombre_usuario": self.nombre_usuario.get(),
            "password": self.password.get()
        }

        # Validaciones básicas
        if not datos["cedula"] or not datos["primer_nombre"] or not datos["primer_apellido"]:
            messagebox.showerror("❌ Error", "Cédula, primer nombre y primer apellido son obligatorios")
            return

        if len(datos["telefono"]) != 11 or not datos["telefono"].isdigit():
            messagebox.showerror("❌ Error", "El teléfono debe tener exactamente 11 dígitos")
            return

        if not datos["nombre_usuario"] or not datos["password"]:
            messagebox.showerror("❌ Error", "Nombre de usuario y contraseña son obligatorios")
            return

        try:
            persona_id = self.model.agregar_personal(**datos)
            if persona_id:
                messagebox.showinfo("✅ Éxito", f"👤 Personal registrado correctamente.\n\n🆔 ID asignado: {persona_id}\n👤 Usuario: {datos['nombre_usuario']}")
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
if __name__ == "__main__":
    vista = PersonalVista()
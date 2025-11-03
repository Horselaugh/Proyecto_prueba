from models_login_nuevo import UserModel
from views_login_nuevo import LoginView
import tkinter.messagebox as msg

class LoginController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView(self)
        self.view.mainloop()

    def handle_login(self, username, password):
        role = self.model.validate_user(username, password)
        if role:
            msg.showinfo("Acceso concedido", f"Bienvenido {username}. Rol: {role}")
        else:
            msg.showerror("Error", "Usuario o contraseña incorrectos") 
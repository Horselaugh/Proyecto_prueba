from typing import List, Dict, Optional
import sys
import os

# Agregar las carpetas al path de Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

from configuracion_model import ConfiguracionModel
import tkinter.messagebox as messagebox

class ConfiguracionController:
    """
    Controlador para el módulo de configuración
    """
    
    def __init__(self):
        self.model = ConfiguracionModel()
    
    def obtener_roles(self) -> List[Dict]:
        """Obtiene todos los roles formateados"""
        roles_db = self.model.obtener_todos_los_roles()
        return [dict(rol) for rol in roles_db]
    
    def crear_rol(self, nombre: str, descripcion: str = "") -> bool:
        """Crea un nuevo rol"""
        if not nombre.strip():
            messagebox.showerror("Error", "El nombre del rol no puede estar vacío.")
            return False
        
        rol_id = self.model.insertar_rol(nombre.strip(), descripcion)
        if rol_id:
            messagebox.showinfo("Éxito", f"Rol '{nombre}' creado correctamente.")
            return True
        else:
            messagebox.showerror("Error", f"No se pudo crear el rol '{nombre}'.")
            return False
    
    def actualizar_rol(self, rol_id: int, nuevo_nombre: str, nueva_descripcion: str = "") -> bool:
        """Actualiza un rol existente"""
        if not nuevo_nombre.strip():
            messagebox.showerror("Error", "El nombre del rol no puede estar vacío.")
            return False
        
        try:
            if self.model.modificar_rol(rol_id, nuevo_nombre.strip(), nueva_descripcion):
                messagebox.showinfo("Éxito", f"Rol actualizado correctamente.")
                return True
            else:
                messagebox.showerror("Error", "No se pudo actualizar el rol.")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar rol: {e}")
            return False
    
    def eliminar_rol(self, rol_id: int, nombre_rol: str) -> bool:
        """Elimina un rol"""
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el rol '{nombre_rol}'? Esta acción es irreversible."
        )
        
        if not confirmacion:
            return False
        
        try:
            if self.model.eliminar_rol(rol_id):
                messagebox.showinfo("Éxito", f"Rol '{nombre_rol}' eliminado correctamente.")
                return True
            else:
                messagebox.showerror("Error", "No se pudo eliminar el rol.")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar rol: {e}")
            return False
    
    def obtener_usuarios(self) -> List[Dict]:
        """Obtiene todos los usuarios formateados"""
        usuarios_db = self.model.obtener_todos_los_usuarios()
        return [dict(usuario) for usuario in usuarios_db]
    
    def crear_usuario(self, datos_usuario: Dict) -> bool:
        """Crea un nuevo usuario"""
        # Validaciones
        campos_requeridos = ['primer_nombre', 'primer_apellido', 'documento_identidad', 'direccion']
        for campo in campos_requeridos:
            if not datos_usuario.get(campo, '').strip():
                messagebox.showerror("Error", f"El campo '{campo.replace('_', ' ').title()}' es obligatorio.")
                return False
        
        try:
            usuario_id = self.model.insertar_usuario(datos_usuario)
            if usuario_id:
                messagebox.showinfo("Éxito", f"Usuario '{datos_usuario['primer_nombre']}' creado correctamente.")
                return True
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario.")
                return False
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {e}")
            return False
    
    def actualizar_usuario(self, datos_usuario: Dict) -> bool:
        """Actualiza un usuario existente"""
        # Validaciones
        campos_requeridos = ['primer_nombre', 'primer_apellido', 'documento_identidad', 'direccion']
        for campo in campos_requeridos:
            if not datos_usuario.get(campo, '').strip():
                messagebox.showerror("Error", f"El campo '{campo.replace('_', ' ').title()}' es obligatorio.")
                return False
        
        try:
            if self.model.modificar_usuario(datos_usuario):
                messagebox.showinfo("Éxito", f"Usuario '{datos_usuario['primer_nombre']}' actualizado correctamente.")
                return True
            else:
                messagebox.showerror("Error", "No se pudo actualizar el usuario.")
                return False
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar usuario: {e}")
            return False
    
    def eliminar_usuario(self, persona_id: int, nombre_usuario: str) -> bool:
        """Elimina un usuario"""
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al usuario '{nombre_usuario}' y todos sus datos personales? Esta acción es irreversible."
        )
        
        if not confirmacion:
            return False
        
        try:
            if self.model.eliminar_usuario(persona_id):
                messagebox.showinfo("Éxito", f"Usuario '{nombre_usuario}' eliminado correctamente.")
                return True
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario: {e}")
            return False
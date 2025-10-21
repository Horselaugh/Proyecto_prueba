import sys
import os
import customtkinter as ctk
from tkinter import messagebox
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from controllers.seguimiento_controller import registrar_seguimiento, listar_seguimientos
except Exception as e:
    registrar_seguimiento = None
    listar_seguimientos = None
    _import_error = e
else:
    _import_error = None

def _intentar_cargar_expedientes():
    try:
        import controllers.expediente_controller as exp_ctrl
        for fn in ("listar_todas", "listar_todos", "listar", "leer"):
            if hasattr(exp_ctrl, fn):
                try:
                    data = getattr(exp_ctrl, fn)()
                    opciones = []
                    for r in data:
                        if isinstance(r, dict) or hasattr(r, "keys"):
                            eid = r.get("id") or r.get("expediente_id") or r.get("id_expediente")
                            desc = r.get("numero") or r.get("titulo") or r.get("descripcion") or str(eid)
                        else:
                            eid = r[0]
                            desc = r[1] if len(r) > 1 else str(eid)
                        opciones.append((eid, f"{eid} - {desc}"))
                    return opciones
                except Exception:
                    continue
    except Exception:
        pass
    return None

def main():
    if _import_error:
        messagebox.showwarning("Aviso módulo seguimientos", f"Error al importar controlador de seguimientos:\n{_import_error}\n\nAsegúrate de agregar controllers/seguimiento_controller.py y models/seguimiento_model.py")
        return

    ventana = ctk.CTkToplevel()
    ventana.title("📌 Seguimiento de Expedientes")
    ventana.geometry("1100x700")
    ventana.configure(fg_color="#1e1e1e")

    frame_principal = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(frame_principal, text="📌 Módulo de Seguimiento de Expedientes", font=("Arial", 22, "bold")).pack(pady=10)

    tabview = ctk.CTkTabview(frame_principal, width=1000, height=520)
    tabview.pack(pady=10, padx=10, fill="both", expand=True)
    tabview.add("Registrar")
    tabview.add("Historial")

    tab_reg = tabview.tab("Registrar")
    opciones_expedientes = _intentar_cargar_expedientes()
    ctk.CTkLabel(tab_reg, text="Expediente (ID o seleccionar):", anchor="w").pack(fill="x", padx=20, pady=(12,4))
    if opciones_expedientes:
        valores = [op[1] for op in opciones_expedientes]
        combo = ctk.CTkComboBox(tab_reg, values=valores, width=600)
        combo.pack(padx=20, pady=4)
    else:
        combo = None
        id_entry = ctk.CTkEntry(tab_reg, placeholder_text="ID del expediente (por ejemplo: 123)", width=300)
        id_entry.pack(padx=20, pady=4)

    frame_fecha = ctk.CTkFrame(tab_reg, fg_color="transparent")
    frame_fecha.pack(fill="x", padx=20, pady=6)
    fecha_entry = ctk.CTkEntry(frame_fecha, placeholder_text="YYYY-MM-DD (opcional)", width=200)
    fecha_entry.pack(side="left", padx=(0,8))
    def poner_hoy():
        fecha_entry.delete(0, "end")
        fecha_entry.insert(0, date.today().strftime("%Y-%m-%d"))
    ctk.CTkButton(frame_fecha, text="Hoy", width=60, command=poner_hoy).pack(side="left")

    ctk.CTkLabel(tab_reg, text="Comentario:", anchor="w").pack(fill="x", padx=20, pady=(8,4))
    comentario_txt = ctk.CTkTextbox(tab_reg, height=8)
    comentario_txt.pack(fill="x", padx=20, pady=4)

    def _registrar():
        try:
            if combo:
                sel = combo.get()
                if not sel:
                    messagebox.showerror("Error", "Seleccione un expediente o ingrese un ID.")
                    return
                expediente_id = int(str(sel).split(" - ")[0])
            else:
                val = id_entry.get().strip()
                if not val:
                    messagebox.showerror("Error", "Ingrese el ID del expediente.")
                    return
                expediente_id = int(val)
        except Exception:
            messagebox.showerror("Error", "ID de expediente inválido.")
            return

        comentario = comentario_txt.get("0.0", "end").strip()
        if not comentario:
            if not messagebox.askyesno("Confirmar", "El comentario está vacío. ¿Deseas registrar sin comentario?"):
                return

        fecha = fecha_entry.get().strip() or None
        try:
            nid = registrar_seguimiento(expediente_id, comentario, fecha)
            messagebox.showinfo("Registro exitoso", f"Seguimiento registrado (id={nid}).")
            comentario_txt.delete("0.0", "end")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el seguimiento:\n{e}")

    ctk.CTkButton(tab_reg, text="Registrar seguimiento", width=220, command=_registrar).pack(pady=12)

    tab_hist = tabview.tab("Historial")

    filtro_frame = ctk.CTkFrame(tab_hist, fg_color="transparent")
    filtro_frame.pack(fill="x", padx=20, pady=8)

    ctk.CTkLabel(filtro_frame, text="Expediente ID (opcional):").grid(row=0, column=0, padx=6, pady=6, sticky="w")
    filtro_id = ctk.CTkEntry(filtro_frame, width=140)
    filtro_id.grid(row=0, column=1, padx=6, pady=6)

    ctk.CTkLabel(filtro_frame, text="Desde (YYYY-MM-DD):").grid(row=0, column=2, padx=6, pady=6, sticky="w")
    filtro_desde = ctk.CTkEntry(filtro_frame, width=140)
    filtro_desde.grid(row=0, column=3, padx=6, pady=6)

    ctk.CTkLabel(filtro_frame, text="Hasta (YYYY-MM-DD):").grid(row=0, column=4, padx=6, pady=6, sticky="w")
    filtro_hasta = ctk.CTkEntry(filtro_frame, width=140)
    filtro_hasta.grid(row=0, column=5, padx=6, pady=6)

    def _buscar():
        eid = filtro_id.get().strip()
        eid_val = int(eid) if eid else None
        desde = filtro_desde.get().strip() or None
        hasta = filtro_hasta.get().strip() or None
        try:
            filas = listar_seguimientos(expediente_id=eid_val, desde=desde, hasta=hasta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener el historial:\n{e}")
            return

        for w in resultados_frame.winfo_children():
            w.destroy()

        if not filas:
            ctk.CTkLabel(resultados_frame, text="No hay registros para los parámetros indicados.").pack(pady=12)
            return

        for idx, r in enumerate(filas):
            texto = f"ID: {r['id']} | EXP: {r['expediente_id']} | FECHA: {r['fecha']} | REG: {r['creado_en']}\n{r['comentario']}"
            lbl = ctk.CTkLabel(resultados_frame, text=texto, anchor="w", justify="left")
            lbl.pack(fill="x", padx=8, pady=(6 if idx==0 else 3,3))

    ctk.CTkButton(filtro_frame, text="Filtrar", command=_buscar).grid(row=0, column=6, padx=8, pady=6)

    resultados_frame = ctk.CTkScrollableFrame(tab_hist, width=980, height=420)
    resultados_frame.pack(padx=20, pady=8, fill="both", expand=True)

    try:
        inicial = listar_seguimientos()
        if inicial:
            for r in inicial:
                texto = f"ID: {r['id']} | EXP: {r['expediente_id']} | FECHA: {r['fecha']} | REG: {r['creado_en']}\n{r['comentario']}"
                ctk.CTkLabel(resultados_frame, text=texto, anchor="w", justify="left").pack(fill="x", padx=8, pady=6)
        else:
            ctk.CTkLabel(resultados_frame, text="No hay registros aún.").pack(pady=12)
    except Exception:
        pass

    ventana.grab_set()
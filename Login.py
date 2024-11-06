import customtkinter as ctk 
from tkinter import messagebox
import tkinter as tk
#Se tiene que cargar los dos valores el final y el inicial, y los campos deben ser variables que se calculan en base al los valores de inicio y final


# Crear la ventana principal
app = ctk.CTk()
app.geometry("300x320")
app.title("Inicio de Sesión")

# Crear los widgets
label_usuario = ctk.CTkLabel(app, text="Usuario:")
label_usuario.pack(pady=10)

entry_usuario = ctk.CTkEntry(app)
entry_usuario.pack(pady=10)

label_contraseña = ctk.CTkLabel(app, text="Contraseña:")
label_contraseña.pack(pady=10)

entry_contraseña = ctk.CTkEntry(app, show="*")
entry_contraseña.pack(pady=10)

# Credenciales correctas
usuario_correcto = "a"
contraseña_correcta = "a"

def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    
    if usuario == usuario_correcto and contraseña == contraseña_correcta:
        messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
        abrir_menu_principal()
    else:
        messagebox.showerror("Inicio de Sesión", "Usuario o contraseña incorrectos")

boton_iniciar_sesion = ctk.CTkButton(app, text="Iniciar Sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack(pady=20)

def abrir_menu_principal():
    menu_principal = ctk.CTkToplevel()
    menu_principal.geometry("400x300")
    menu_principal.title("Menú Principal")
    
    label_bienvenida = ctk.CTkLabel(menu_principal, text="Bienvenido al Menú Principal")
    label_bienvenida.pack(pady=20)
    
    ingresar_btn = ctk.CTkButton(menu_principal, text="Ingresar", font=("Arial", 16), command=mostrar_pantalla_opciones)
    ingresar_btn.pack(pady=10)

def mostrar_pantalla_opciones():
    for widget in app.winfo_children():
        widget.destroy()
    
    ctk.CTkLabel(app, text="Seleccione una opción", font=("Arial", 16)).pack(pady=10)

    calcular_btn = ctk.CTkButton(app, text="Calcular", font=("Arial", 16), command=mostrar_pantalla_calculo)
    calcular_btn.pack(pady=10)

    imprimir_ventas_btn = ctk.CTkButton(app, text="Imprimir Ventas", font=("Arial", 16))
    imprimir_ventas_btn.pack(pady=10)

def mostrar_pantalla_calculo():
    for widget in app.winfo_children():
        widget.destroy()

    ctk.CTkLabel(app, text="Calcular Total de Factura", font=("Arial", 16)).pack(pady=1)

    # Campos de entrada para cada concepto
    app.campos = {}
    conceptos = [
        "Cargo Fijo por Suministro", "Consumo primeros 600 KWh", "Consumo excedente 142 KWh",
        "Consumo excedente 43 KWh", "Consumo excedente 503 KWh", "Beneficio Social Provincial",
        "Subsidio", "Consumo Bimestral", "Alumbrado Público", "IVA (21%)"
    ]

    for concepto in conceptos:
        label = ctk.CTkLabel(app, text=concepto)
        label.pack()
        entry = ctk.CTkEntry(app)
        entry.pack(pady=1)
        app.campos[concepto] = entry

    calcular_btn = ctk.CTkButton(app, text="Calcular Total", command=calcular_total)
    calcular_btn.pack(pady=1)

    app.total_label = ctk.CTkLabel(app, text="Total Bimestral: ", font=("Arial", 14))
    app.total_label.pack(pady=1)

def calcular_total():
    try:
        total = sum(int(entry.get() or 0) for entry in app.campos.values())
        app.total_label.configure(text="Total Bimestral: ${}".format(total))
    except ValueError as e:
        messagebox.showwarning("Error", f"Por favor ingresa valores numéricos válidos en todos los campos. Error: {e}")


# Ejecutar la aplicación
app.mainloop()

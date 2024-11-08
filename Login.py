import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

# Crear la ventana principal
app = ctk.CTk()
app.geometry("300x320")
app.title("Inicio de Sesión")

# Credenciales correctas
usuario_correcto = "a"
contraseña_correcta = "a"

# Función para iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    
    if usuario == usuario_correcto and contraseña == contraseña_correcta:
        messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
        mostrar_pantalla_opciones()
    else:
        messagebox.showerror("Inicio de Sesión", "Usuario o contraseña incorrectos")

# Función para mostrar la pantalla de opciones
def mostrar_pantalla_opciones():
    limpiar_pantalla()

    ctk.CTkLabel(app, text="Seleccione una opción", font=("Arial", 16)).pack(pady=10)

    calcular_btn = ctk.CTkButton(app, text="Calcular", font=("Arial", 16), command=mostrar_pantalla_calculo)
    calcular_btn.pack(pady=10)

    imprimir_ventas_btn = ctk.CTkButton(app, text="Imprimir Ventas", font=("Arial", 16))
    imprimir_ventas_btn.pack(pady=10)

# Función para mostrar la pantalla de cálculo de consumo
def mostrar_pantalla_calculo():
    limpiar_pantalla()

    ctk.CTkLabel(app, text="Ingrese lectura inicial (kWh):").pack(pady=5)
    global entry_inicial, entry_final
    entry_inicial = ctk.CTkEntry(app)
    entry_inicial.pack(pady=5)

    ctk.CTkLabel(app, text="Ingrese lectura final (kWh):").pack(pady=5)
    entry_final = ctk.CTkEntry(app)
    entry_final.pack(pady=5)

    # Botón para calcular
    boton_calcular = ctk.CTkButton(app, text="Calcular Consumo", command=calcular_consumo)
    boton_calcular.pack(pady=10)

    # Etiqueta para mostrar el resultado
    global total_label_iva
    global total_label1
    global total_label2
    global total_label3
    global total_label4

    total_label1 = ctk.CTkLabel(app, text="Rango 1: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    total_label2 = ctk.CTkLabel(app, text="Rango 2 Total: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    total_label3 = ctk.CTkLabel(app, text="Rango 3: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    total_label4 = ctk.CTkLabel(app, text="Rango 3: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    total_label_iva = ctk.CTkLabel(app, text="Consumo Total: 0 kWh\nCosto Total con iva(%21): $0.00", font=("Arial", 14))

    total_label_iva.pack(pady=20)
    total_label1.pack(pady=20)
    total_label2.pack(pady=20)
    total_label3.pack(pady=20)
    total_label4.pack(pady=20)

# Función para calcular el consumo
def calcular_consumo():
    # Tarifas de DPEC en ARS por kWh
    TARIFA_BASE = 123.9694  # Primeros 600 kWh
    TARIFA_EXCEDENTE_1 = 134.8474  # Excedente de 600 a 742 kWh (142 kWh)
    TARIFA_EXCEDENTE_2 = 162.1050  # Excedente de 742 a 785 kWh (43 kWh)
    TARIFA_EXCEDENTE_3 = 166.6580  # Excedente mayor a 785 kWh

    try:
        inicial = float(entry_inicial.get())
        final = float(entry_final.get())
        consumo_total = final - inicial

        # Variables para almacenar el consumo en cada rango
        rango1 = min(consumo_total, 600)  # Primeros 600 kWh
        rango2 = max(min(consumo_total - 600, 142), 0)  # Excedente de 600 a 742 kWh
        rango3 = max(min(consumo_total - 742, 43), 0)  # Excedente de 742 a 785 kWh
        rango4 = max(consumo_total - 785, 0)  # Excedente mayor a 785 kWh

        # Cálculo de costos
        costo_rango1 = rango1 * TARIFA_BASE
        costo_rango2 = rango2 * TARIFA_EXCEDENTE_1
        costo_rango3 = rango3 * TARIFA_EXCEDENTE_2
        costo_rango4 = rango4 * TARIFA_EXCEDENTE_3
        costo_total = costo_rango1 + costo_rango2 + costo_rango3 + costo_rango4

        # Mostrar resultado en la etiqueta
        texto_rango1 = f"Rango 1: {rango1} kWh\nCosto Rango 1: ${costo_rango1:.2f}"
        texto_rango2 = f"Rango 2: {rango2} kWh\nCosto Rango 2: ${costo_rango2:.2f}"
        texto_rango3 = f"Rango 3: {rango3} kWh\nCosto Rango 3: ${costo_rango3:.2f}"
        texto_rango4 = f"Rango 4: {rango4} kWh\nCosto Rango 4: ${costo_rango4:.2f}"
        total_iva = f"Consumo Total con iva: {consumo_total + consumo_total * 0.21} kWh\nCosto Total: ${costo_total:.2f}"

        
        
        total_label1.configure(text=texto_rango1)
        total_label2.configure(text=texto_rango2)
        total_label3.configure(text=texto_rango3)
        total_label4.configure(text=texto_rango4)
        total_label_iva.configure(text=total_iva)


    except ValueError:
        messagebox.showwarning("Error", "Por favor ingrese valores numéricos válidos.")

# Función para limpiar la pantalla actual
def limpiar_pantalla():
    for widget in app.winfo_children():
        widget.pack_forget()

# Widgets de inicio de sesión
label_usuario = ctk.CTkLabel(app, text="Usuario:")
label_usuario.pack(pady=10)

entry_usuario = ctk.CTkEntry(app)
entry_usuario.pack(pady=10)

label_contraseña = ctk.CTkLabel(app, text="Contraseña:")
label_contraseña.pack(pady=10)

entry_contraseña = ctk.CTkEntry(app, show="*")
entry_contraseña.pack(pady=10)

boton_iniciar_sesion = ctk.CTkButton(app, text="Iniciar Sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack(pady=20)

# Ejecutar la aplicación
app.mainloop()

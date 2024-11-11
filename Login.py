import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
# Crear la ventana principal
app = ctk.CTk()
app.geometry("300x320")
app.title("Inicio de Sesión")

# Credenciales correctas
usuario_correcto = "a"
contraseña_correcta = "a"

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Crear los marcos
frame_inicio = ctk.CTkFrame(app)
frame_calcular = ctk.CTkFrame(app)
frame_consumo = ctk.CTkFrame(app)

frame_imprimir = ctk.CTkFrame(app)
frame_opciones = ctk.CTkFrame(app)

def volver_inicio():
    frame_calcular.pack_forget()
    frame_imprimir.pack_forget()
    frame_opciones.pack_forget()
    frame_inicio.pack()

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
    limpiar_frame(frame_opciones)
    frame_opciones.pack()

    ctk.CTkLabel(frame_opciones, text="Seleccione una opción", font=("Arial", 16)).pack(pady=10)

    calcular_btn = ctk.CTkButton(frame_opciones, text="Calcular", font=("Arial", 16), command=mostrar_pantalla_calculo)
    calcular_btn.pack(pady=10)

    imprimir_ventas_btn = ctk.CTkButton(frame_opciones, text="Imprimir Ventas", font=("Arial", 16), command=mostrar_pantalla_imprimir)
    imprimir_ventas_btn.pack(pady=10)

# Función para mostrar la pantalla de cálculo de consumo
def mostrar_pantalla_calculo():
    limpiar_pantalla()
    limpiar_frame(frame_calcular)

    frame_calcular.pack()

    ctk.CTkLabel(frame_calcular, text="Ingrese lectura inicial (kWh):").pack(pady=5)
    global entry_inicial, entry_final
    entry_inicial = ctk.CTkEntry(frame_calcular)
    entry_inicial.pack(pady=5)

    ctk.CTkLabel(frame_calcular, text="Ingrese lectura final (kWh):").pack(pady=5)
    entry_final = ctk.CTkEntry(frame_calcular)
    entry_final.pack(pady=5)

    boton_calcular = ctk.CTkButton(frame_calcular, text="Calcular Consumo", command=calcular_consumo)
    boton_calcular.pack(pady=10)

    global monto_label1, monto_label2, monto_label3, monto_label4, alumbrado_publico, label_iva, total_final_label

    monto_label1 = ctk.CTkLabel(frame_calcular, text="Consumo primeros 600 kWh: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    monto_label2 = ctk.CTkLabel(frame_calcular, text="Consumo excedente de 600 KWh: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    monto_label3 = ctk.CTkLabel(frame_calcular, text="Consumo excedente de 600 KWh: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    monto_label4 = ctk.CTkLabel(frame_calcular, text="Consumo excedente de 600 KWh: 0 kWh\nCosto Total: $0.00", font=("Arial", 14))
    alumbrado_publico = ctk.CTkLabel(frame_calcular, text="Alumbrado Publico: $0.00", font=("Arial", 14))
    label_iva = ctk.CTkLabel(frame_calcular, text="IVA: $0.00", font=("Arial", 14))
    total_final_label = ctk.CTkLabel(frame_calcular, text="Consumo Total: 0 kWh\nCosto Total con IVA: $0.00", font=("Arial", 14))

    monto_label1.pack(pady=5)
    monto_label2.pack(pady=5)
    monto_label3.pack(pady=5)
    monto_label4.pack(pady=5)
    alumbrado_publico.pack(pady=5)
    label_iva.pack(pady=5)
    total_final_label.pack(pady=5)

    volver_btn_calcular = ctk.CTkButton(frame_calcular, text="Volver", command=mostrar_pantalla_opciones)
    volver_btn_calcular.pack(pady=10)

# Función para mostrar la pantalla de impresión de ventas
def mostrar_pantalla_imprimir():
    limpiar_pantalla()
    limpiar_frame(frame_imprimir)

    frame_imprimir.pack()

    ctk.CTkLabel(frame_imprimir, text="Pantalla de Imprimir Ventas", font=("Arial", 16)).pack(pady=10)

    # Botón para guardar en PDF
    guardar_pdf_btn = ctk.CTkButton(frame_imprimir, text="Guardar en PDF", command=guardar_en_pdf)
    guardar_pdf_btn.pack(pady=10)

    volver_btn_imprimir = ctk.CTkButton(frame_imprimir, text="Volver", command=mostrar_pantalla_opciones)
    volver_btn_imprimir.pack(pady=10)

# Función para calcular el consumo
def calcular_consumo():
    limpiar_frame(frame_consumo)

   # Tarifas de DPEC por kWh
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
        costo_alumbrado = 4426

        # Mostrar resultado en la etiqueta
        texto_rango1 = f"Consumo primeros 600 kWh a $123.9694: {rango1} kWh\nConsumo primeros: ${costo_rango1:.2f}"
        texto_rango2 = f"Consumo excedente de 600 KWh/bim 142 KWh a $134.8474: {rango2} kWh\nConsumo excedente: ${costo_rango2:.2f}"
        texto_rango3 = f"Consumo excedente de 600 KWh/bim 43 KWh a $162.1050: {rango3} kWh\nConsumo excedente: ${costo_rango3:.2f}"
        texto_rango4 = f"Consumo excedente de 600 KWh/bim 503 KWh a $166.6580: {rango4} kWh\nConsumo excedente: ${costo_rango4:.2f}"
        texto_alumbrado= f"Alumbrado Publico: ${costo_alumbrado:.2f}"
        iva =  costo_total * 0.21
        
        texto_iva = f"IVA consumidor final 21% : {iva}"
        total_final = f"Consumo Total: {consumo_total} kWh\nIva 21%: ${costo_total:.2f}"

        monto_label1.configure(text=texto_rango1)
        monto_label2.configure(text=texto_rango2)
        monto_label3.configure(text=texto_rango3)
        monto_label4.configure(text=texto_rango4)
        alumbrado_publico.configure(text=texto_alumbrado)
        label_iva.configure(text=texto_iva)
        total_final_label.configure(text=total_final)
        

    except ValueError:
        messagebox.showwarning("Error", "Por favor ingrese valores numéricos válidos.")

# Función para limpiar la pantalla actual
def limpiar_pantalla():
    frame_inicio.pack_forget()
    frame_opciones.pack_forget()
    frame_calcular.pack_forget()
    frame_imprimir.pack_forget()



# Widgets de inicio de sesión
frame_inicio.pack()
label_usuario = ctk.CTkLabel(frame_inicio, text="Usuario:")
label_usuario.pack(pady=10)

entry_usuario = ctk.CTkEntry(frame_inicio)
entry_usuario.pack(pady=10)

label_contraseña = ctk.CTkLabel(frame_inicio, text="Contraseña:")
label_contraseña.pack(pady=10)

entry_contraseña = ctk.CTkEntry(frame_inicio, show="*")
entry_contraseña.pack(pady=10)

boton_iniciar_sesion = ctk.CTkButton(frame_inicio, text="Iniciar Sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack(pady=20)


def guardar_en_pdf():
    pdf_path = "calculo_consumo.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Agregar título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 50, "Reporte de Consumo")

    # Agregar los cálculos al PDF
    y = height - 100
    c.setFont("Helvetica", 12)
    c.drawString(50, y, monto_label1.cget("text"))
    y -= 40
    c.drawString(50, y, monto_label2.cget("text"))
    y -= 40
    c.drawString(50, y, monto_label3.cget("text"))
    y -= 40
    c.drawString(50, y, monto_label4.cget("text"))
    y -= 40
    c.drawString(50, y, alumbrado_publico.cget("text"))
    y -= 40
    c.drawString(50, y, label_iva.cget("text"))
    y -= 40
    c.drawString(50, y, total_final_label.cget("text"))

    # Guardar y cerrar el archivo PDF
    c.save()
    messagebox.showinfo("Guardar PDF", f"El reporte ha sido guardado como {pdf_path}")


# Ejecutar la aplicación
app.mainloop()

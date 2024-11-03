from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Factura de Electricidad")
        self.setGeometry(100, 100, 700, 700)
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.initUI()

    def initUI(self):
        # Etiqueta de bienvenida
        self.label = QLabel("¡Bienvenido a Electricidad RodrCfdf!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.layout.addWidget(self.label)

        # Botón de ingresar
        self.ingresar_btn = QPushButton("Ingresar")
        self.ingresar_btn.setStyleSheet("font-size: 20px; background-color: red; color: black;")
        self.ingresar_btn.clicked.connect(self.mostrar_pantalla_opciones)
        self.layout.addWidget(self.ingresar_btn)

    def mostrar_pantalla_opciones(self):
        self.limpiar_layout()
        
        self.label_opciones = QLabel("Seleccione una opción")
        self.label_opciones.setAlignment(Qt.AlignCenter)
        self.label_opciones.setStyleSheet("font-size: 20px; background-color: white; color: black;")
        self.layout.addWidget(self.label_opciones)

        # Botones para opciones
        self.insertar_btn = QPushButton("Calcular")
        self.insertar_btn.setStyleSheet("font-size: 20px; background-color: red; color: black;")
        self.insertar_btn.clicked.connect(self.mostrar_pantalla_calculo)
        self.layout.addWidget(self.insertar_btn)

        self.ver_ventas_btn = QPushButton("Imprimir Ventas")
        self.ver_ventas_btn.setStyleSheet("font-size: 20px; background-color: red; color: black;")
        self.ver_ventas_btn.clicked.connect(self.mostrar_pantalla_ventas)
        self.layout.addWidget(self.ver_ventas_btn)

    def limpiar_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def mostrar_pantalla_ventas(self):
        self.limpiar_layout()

        self.label_ventas = QLabel("Imprimir boleta")
        self.label_ventas.setAlignment(Qt.AlignCenter)
        self.label_ventas.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.label_ventas)

        self.treeview_ventas = QTableWidget()
        self.treeview_ventas.setColumnCount(4)
        self.treeview_ventas.setHorizontalHeaderLabels(["Fecha", "Producto", "Cantidad", "Total"])
        self.layout.addWidget(self.treeview_ventas)

        self.cargar_ventas_del_dia()

    def mostrar_pantalla_calculo(self):
        self.limpiar_layout()

        self.label_calculo = QLabel("Calcular Total de Factura")
        self.label_calculo.setAlignment(Qt.AlignCenter)
        self.label_calculo.setStyleSheet("font-size: 20px; background-color: white; color: black;")
        self.layout.addWidget(self.label_calculo)

        # Campos de entrada para cada concepto
        self.campos = {
            "Cargo Fijo por Suministro": QLineEdit(),
            "Consumo primeros 600 KWh": QLineEdit(),
            "Consumo excedente 142 KWh": QLineEdit(),
            "Consumo excedente 43 KWh": QLineEdit(),
            "Consumo excedente 503 KWh": QLineEdit(),
            "Beneficio Social Provincial": QLineEdit(),
            "Subsidio": QLineEdit(),
            "Consumo Bimestral": QLineEdit(),
            "Alumbrado Público": QLineEdit(),
            "IVA (21%)": QLineEdit(),
        }

        # Agregar los campos al layout
        for label, campo in self.campos.items():
            campo.setPlaceholderText(label)
            self.layout.addWidget(QLabel(label))
            self.layout.addWidget(campo)

        # Botón para calcular
        self.calcular_btn = QPushButton("Calcular Total")
        self.calcular_btn.clicked.connect(self.calcular_total)
        self.layout.addWidget(self.calcular_btn)

        # Etiqueta para mostrar el total
        self.total_label = QLabel("Total Bimestral: ")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.total_label)

    def calcular_total(self):
        try:
            # Obtener los valores de cada campo, convirtiendo a float
            total = 0
            for label, campo in self.campos.items():
                valor = campo.text()
                if valor:
                    total += float(valor)
                    
            # Mostrar el total
            self.total_label.setText(f"Total Bimestral: ${total:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingresa valores numéricos válidos en todos los campos.")

    def cargar_ventas_del_dia(self):
        # Aquí iría la lógica de conexión a la base de datos
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
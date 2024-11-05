from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QMessageBox, QComboBox,QDialog,QMainWindow
)
from PyQt5.QtCore import Qt
import sys
class LoginScreen(QDialog):
    def __init__(self, main_screen):
        super().__init__(main_screen)
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 300)
        self.setStyleSheet("background-color: grey;")

        # Etiqueta de instrucciones
        label_instructions = QLabel("Por favor, ingrese los datos")
        label_instructions.setStyleSheet("background-color: skyblue;")
        label_instructions.setAlignment(Qt.AlignCenter)

        # Espaciado
        label_space_1 = QLabel()
        label_space_1.setStyleSheet("background-color: grey;")

        # Campos de entrada
        self.dni_verify = QLineEdit()
        self.dni_verify.setPlaceholderText("45053765")

        label_space_2 = QLabel()
        label_space_2.setStyleSheet("background-color: grey;")

        self.password_verify = QLineEdit()
        self.password_verify.setPlaceholderText("1234")
        self.password_verify.setEchoMode(QLineEdit.Password)

        # Botón de login
        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: skyblue;")
        login_button.clicked.connect(self.login_verify)

        # Espaciado
        label_space_3 = QLabel()
        label_space_3.setStyleSheet("background-color: grey;")

        # Botón para volver
        back_button = QPushButton("Volver")
        back_button.setStyleSheet("background-color: skyblue;")
        back_button.clicked.connect(self.close)

        # Layout de la ventana
        layout = QVBoxLayout()
        layout.addWidget(label_instructions)
        layout.addWidget(label_space_1)
        layout.addWidget(QLabel("Número D.N.I"))
        layout.addWidget(self.dni_verify)
        layout.addWidget(label_space_2)
        layout.addWidget(QLabel("Contraseña"))
        layout.addWidget(self.password_verify)
        layout.addWidget(label_space_3)
        layout.addWidget(login_button)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def login_verify(self):
        dni = self.dni_verify.text()
        password = self.password_verify.text()
        
        # Lógica de verificación de usuario (puede ser una conexión a base de datos)
        if dni == "1234" and password == "admin":  # Ejemplo de credenciales
            QMessageBox.information(self, "Login", "Inicio de sesión exitoso")
            self.accept()  # Cierra la pantalla de login con éxito
        else:
            QMessageBox.warning(self, "Login", "D.N.I o contraseña incorrectos")

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
class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        self.setCentralWidget(self.main_window)

    def iniciar_con_login(self):
        login_screen = LoginScreen(self)
        if login_screen.exec_() == QDialog.Accepted:
            self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.iniciar_con_login()
    sys.exit(app.exec_())
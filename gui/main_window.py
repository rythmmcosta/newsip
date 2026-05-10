from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QFormLayout, QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setWindowTitle("NewSIP - MicroSIP Clone")
        self.setFixedSize(300, 450)

        # UI Components
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Registration Section
        self.reg_form = QFormLayout()
        self.server_input = QLineEdit("sip.example.com")
        self.user_input = QLineEdit("username")
        self.pass_input = QLineEdit("password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.reg_form.addRow("Server:", self.server_input)
        self.reg_form.addRow("User:", self.user_input)
        self.reg_form.addRow("Pass:", self.pass_input)
        
        self.reg_btn = QPushButton("Login")
        self.reg_btn.clicked.connect(self.handle_register)
        
        self.layout.addLayout(self.reg_form)
        self.layout.addWidget(self.reg_btn)

        self.layout.addSpacing(20)

        # Dialer Section
        self.dial_input = QLineEdit()
        self.dial_input.setPlaceholderText("sip:user@domain or number")
        self.layout.addWidget(self.dial_input)

        self.btn_layout = QHBoxLayout()
        self.call_btn = QPushButton("Call")
        self.call_btn.setStyleSheet("background-color: green; color: white;")
        self.call_btn.clicked.connect(self.handle_call)
        
        self.hang_btn = QPushButton("Hangup")
        self.hang_btn.setStyleSheet("background-color: red; color: white;")
        self.hang_btn.clicked.connect(self.handle_hangup)
        
        self.btn_layout.addWidget(self.call_btn)
        self.btn_layout.addWidget(self.hang_btn)
        self.layout.addLayout(self.btn_layout)

        # Status Label
        self.status_label = QLabel("Status: Idle")
        self.layout.addWidget(self.status_label)
        
        self.setup_tray()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        # For real app, you'd load an icon here
        # self.tray_icon.setIcon(QIcon("icon.png"))
        
        tray_menu = QMenu()
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(sys.exit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def handle_register(self):
        try:
            self.engine.register(self.server_input.text(), self.user_input.text(), self.pass_input.text())
            self.status_label.setText("Status: Registering...")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def handle_call(self):
        try:
            self.engine.make_call(self.dial_input.text())
            self.status_label.setText(f"Status: Calling {self.dial_input.text()}")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def handle_hangup(self):
        try:
            self.engine.hangup()
            self.status_label.setText("Status: Hanging up...")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("NewSIP", "App minimized to tray", QSystemTrayIcon.Information, 2000)

import sys
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget
from PyQt5.QtCore import QTimer, Qt
import configparser
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.results = []

        config = configparser.ConfigParser()
        config.read('config.ini')

        text_button = config['Config']['button']
        text_title = config['Config']['title']

        key_value = list(config['NumberWeights'].keys())
        self.results = key_value
        key_weights = self.weights = [float(config['NumberWeights'][x]) for x in self.results]

        self.numbers = key_value
        self.weights = key_weights
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 32))
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button = QPushButton(text_button, self)
        self.button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button.setFont(QFont("Arial", 18))
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button.clicked.connect(self.on_button_click)
        
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setStyleSheet("background-color: #FF5252; color: white;")
        self.quit_button.setFont(QFont("Arial", 18))
        self.quit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.quit_button.clicked.connect(QApplication.quit)


        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.label)
        hbox.addStretch()
        
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.button)
        hbox_buttons.addWidget(self.quit_button)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_buttons)
        
        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.setInterval(100)

        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QColor("#ECEFF1"))
        self.setPalette(self.palette)

        pixmap = QPixmap("icon.jpg")
        self.setWindowIcon(pixmap)

        self.setWindowTitle(text_title)

    def weighted_random_choice(self, choices, weights):
        total = sum(weights)
        r = random.uniform(0, total)
        upto = 0
        for c, w in zip(choices, weights):
            if upto + w >= r:
                return c
            upto += w

    def on_button_click(self):
        self.timer.start()

    def on_timer_tick(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        text_value = config['Config']['resultMessage']

        result = str(self.weighted_random_choice(self.numbers, self.weights))
        self.label.setText(result)
        self.results.append(result)

        self.label.setAlignment(Qt.AlignCenter)

        if len(self.results) >= 10:
            if result == str(self.weighted_random_choice(self.numbers, self.weights)):
                self.results = []  
                self.timer.stop()
                self.label.setText(f"{text_value}{result}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setGeometry(100, 100, 350, 200)
    main_window.show()
    sys.exit(app.exec_())

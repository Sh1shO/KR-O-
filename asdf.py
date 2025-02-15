import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class HarryPotterApp(QMainWindow):
    API_URL = "https://potterapi-fedeperin.vercel.app/en/characters"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Гарри Поттер - Персонажи")
        self.setGeometry(100, 100, 720, 820)
        self.data = []
        self.filtered_data = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        self.setWindowIcon(QIcon("/home/KHPK.RU/student/Загрузки/HarryPoter.png"))

        search_layout = QHBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Поиск по полному имени")
        self.search_name.textChanged.connect(self.filter_data)

        self.search_actor = QLineEdit()
        self.search_actor.setPlaceholderText("Поиск по актеру")
        self.search_actor.textChanged.connect(self.filter_data)

        search_layout.addWidget(self.search_name)
        search_layout.addWidget(self.search_actor)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Полное имя", "Никнейм", "Факультет", "Актер", "Дата рождения"])
        self.table.setSortingEnabled(True)

        layout.addLayout(search_layout)
        layout.addWidget(self.table)

        central_widget.setLayout(layout)

    def load_data(self):
        response = requests.get(self.API_URL)
        if response.status_code == 200:
            self.data = response.json()
            self.filtered_data = self.data
            self.update_table()
        else:
            print("Ошибка загрузки данных")

    def update_table(self):
        self.table.setRowCount(len(self.filtered_data))
        for row, char in enumerate(self.filtered_data):
            print(char)
            fullName = char.get("fullName", "-")
            nickname = char.get("nickname", "-")
            hogwartsHouse = char.get("hogwartsHouse", "-")
            interpretedBy = char.get("interpretedBy", "-")
            birthdate = char.get("birthdate", "-")

            self.table.setItem(row, 0, QTableWidgetItem(fullName))
            self.table.setItem(row, 1, QTableWidgetItem(nickname))
            self.table.setItem(row, 2, QTableWidgetItem(hogwartsHouse))
            self.table.setItem(row, 3, QTableWidgetItem(interpretedBy))
            self.table.setItem(row, 4, QTableWidgetItem(birthdate))

        self.table.resizeColumnsToContents()

    def filter_data(self):
        name_filter = self.search_name.text().strip().lower()
        actor_filter = self.search_actor.text().strip().lower()

        self.filtered_data = [
            char for char in self.data
            if (not name_filter or name_filter in char.get("fullName", "").lower()) and
               (not actor_filter or actor_filter in char.get("interpretedBy", "").lower())
        ]
        self.update_table()

app = QApplication([])
window = HarryPotterApp()
window.show()
app.exec()


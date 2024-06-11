import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt
from service_table_widget import ServiceTableWidget
from utility import apply_dark_mode, apply_light_mode


class ServiceManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Service Manager')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search Service:")
        self.search_input = QLineEdit()
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        # Dark mode toggle
        self.dark_mode_check = QCheckBox("Dark Mode")
        self.dark_mode_check.stateChanged.connect(self.toggle_dark_mode)
        search_layout.addWidget(self.dark_mode_check)

        main_layout.addLayout(search_layout)

        # Table for services
        self.service_table = ServiceTableWidget(self.search_input)
        main_layout.addWidget(self.service_table)

        self.setLayout(main_layout)

        self.search_input.textChanged.connect(self.service_table.filter_services)

    def toggle_dark_mode(self, state):
        if state == Qt.Checked:
            apply_dark_mode(app)
        else:
            apply_light_mode(app)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServiceManagerApp()
    ex.show()
    sys.exit(app.exec_())

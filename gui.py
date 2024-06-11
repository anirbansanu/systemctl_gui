import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
from PyQt5.QtCore import Qt, QSize

class ServiceManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Service Manager')
        self.showMaximized()

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.populate_table()

    def populate_table(self):
        services = self.get_services()

        self.table.setRowCount(len(services))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Service', 'Description', 'Status', 'Start/Stop', 'Enable/Disable'])

        for row, service in enumerate(services):
            service_name, description, status = service

            self.table.setItem(row, 0, QTableWidgetItem(service_name))
            self.table.setItem(row, 1, QTableWidgetItem(description))
            self.table.setItem(row, 2, QTableWidgetItem(status))

            start_stop_btn = QPushButton('Stop' if status == 'running' else 'Start')
            start_stop_btn.setCheckable(True)
            start_stop_btn.setChecked(status == 'running')
            start_stop_btn.setMinimumSize(QSize(100, 30))
            start_stop_btn.clicked.connect(lambda checked, s=service_name: self.toggle_service(checked, s, 'start', 'stop'))
            self.table.setCellWidget(row, 3, start_stop_btn)

            enable_disable_btn = QPushButton('Disable' if 'enabled' in status else 'Enable')
            enable_disable_btn.setCheckable(True)
            enable_disable_btn.setChecked('enabled' in status)
            enable_disable_btn.setMinimumSize(QSize(100, 30))
            enable_disable_btn.clicked.connect(lambda checked, s=service_name: self.toggle_service(checked, s, 'enable', 'disable'))
            self.table.setCellWidget(row, 4, enable_disable_btn)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def get_services(self):
        command = ['systemctl', 'list-units', '--type=service', '--all', '--no-pager']
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        services = []
        lines = result.stdout.splitlines()
        for line in lines[1:]:
            parts = line.split(maxsplit=4)
            if len(parts) < 5:
                continue
            service_name = parts[0]
            status = parts[3]
            description = parts[4] if len(parts) > 4 else ""
            services.append((service_name, description, status))
        return services

    def toggle_service(self, checked, service_name, action_enable, action_disable):
        action = action_enable if checked else action_disable
        self.run_command(['sudo', 'systemctl', action, service_name])
        self.populate_table()

    def run_command(self, command):
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.show_message(result.stdout)
        except subprocess.CalledProcessError as e:
            self.show_message(e.stderr)

    def show_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServiceManagerApp()
    ex.show()
    sys.exit(app.exec_())

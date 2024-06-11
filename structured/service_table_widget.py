from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QMessageBox, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from service_manager_logic import ServiceManager
from utility import run_command


class ServiceTableWidget(QTableWidget):
    def __init__(self, search_input):
        super().__init__()
        self.search_input = search_input
        self.service_manager = ServiceManager()
        self.sort_order = Qt.AscendingOrder
        self.initUI()

    def initUI(self):
        self.populate_table()
        self.horizontalHeader().sectionClicked.connect(self.sort_table)

    def populate_table(self):
        services = self.service_manager.get_services()

        self.setRowCount(len(services))
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['Service', 'Description', 'Status', 'Start/Stop', 'Enable/Disable'])

        for row, service in enumerate(services):
            service_name, description, status = service

            self.setItem(row, 0, QTableWidgetItem(service_name))
            self.setItem(row, 1, QTableWidgetItem(description))
            self.setItem(row, 2, QTableWidgetItem(status))

            start_stop_btn = self.create_button('Stop' if 'running' in status else 'Start',
                                                lambda checked, s=service_name: self.toggle_service(checked, s, 'start', 'stop'),
                                                'running' in status)
            self.setCellWidget(row, 3, start_stop_btn)

            enable_disable_btn = self.create_button('Disable' if 'enabled' in status else 'Enable',
                                                    lambda checked, s=service_name: self.toggle_service(checked, s, 'enable', 'disable'),
                                                    'enabled' in status)
            self.setCellWidget(row, 4, enable_disable_btn)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        # Apply style for better appearance
        self.apply_table_style()

    def create_button(self, text, slot, checked):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setMinimumSize(QSize(80, 30))  # Set a suitable minimum size for buttons
        btn.setMaximumSize(QSize(100, 30))  # Set a suitable maximum size for buttons
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.clicked.connect(slot)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(btn, 0, Qt.AlignCenter)
        container.setLayout(layout)
        return container

    def toggle_service(self, checked, service_name, action_enable, action_disable):
        action = action_enable if checked else action_disable
        result = run_command(['sudo', 'systemctl', action, service_name])
        if result:
            self.populate_table()
            QMessageBox.information(self, "Service Manager", f"Service {service_name} {action}d successfully.")
        else:
            QMessageBox.critical(self, "Service Manager", f"Failed to {action} service {service_name}.")

    def filter_services(self):
        filter_text = self.search_input.text().lower()
        for row in range(self.rowCount()):
            service_name = self.item(row, 0).text().lower()
            self.setRowHidden(row, filter_text not in service_name)

    def sort_table(self, index):
        self.sortItems(index, self.sort_order)
        self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder

    def apply_table_style(self):
        # Set alternating row colors
        self.setAlternatingRowColors(True)
        self.setStyleSheet(
            "QTableWidget::item { padding: 10px; }"
            "QHeaderView::section { background-color: #404040; color: white; }"
            "QTableWidget { gridline-color: #404040; }"
            "QTableWidget::item:selected { background-color: #565656; }"
            "QPushButton { padding: 5px; font-size: 12px; }"
        )
        self.setShowGrid(True)
        self.setGridStyle(Qt.SolidLine)

        # Set the default row height for all rows
        self.verticalHeader().setDefaultSectionSize(50)

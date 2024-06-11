import subprocess
from PyQt5.QtWidgets import QMessageBox
import qdarkstyle
from PyQt5.QtCore import Qt


def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        show_message(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        show_message(e.stderr)
        return False


def show_message(message):
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.exec_()


def apply_dark_mode(app):
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


def apply_light_mode(app):
    app.setStyleSheet("")

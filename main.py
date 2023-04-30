from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
)

from src.ui import Ui_HotelModelUI

if __name__ == "__main__":
    app = QApplication([])
    window = QMainWindow()
    window.setFixedSize(1300, 800)
    ui = Ui_HotelModelUI()
    ui.setupUi(window)
    window.show()
    app.exec()

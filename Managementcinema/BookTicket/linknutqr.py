from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from maqr import Ui_MainWindow


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối nút Xác nhận với hàm thông báo
        self.ui.ButtonXacnhanTT.clicked.connect(self.show_payment_success)

    def show_payment_success(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Thông báo")
        msg.setText("Thanh toán thành công!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

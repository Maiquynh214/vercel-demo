import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QLabel
from maqr import Ui_MainWindow as Ui_QRWindow
# from PyQt6.QtCore import Qt
from cinema import Ui_MainWindow
from hoadon import Ui_MainWindow as HoaDonWindow
from nutthanhtoan import setup_hoadon_button_links

class PaymentProcessor:
    def __init__(self, main_ui):
        self.main_ui = main_ui

    def calculate_total(self):
        ve_gia = len(self.main_ui.selected_seats) * 100000
        bap_mini = self.main_ui.spinBox.value() * 70000
        bap_lon = self.main_ui.spinBox_2.value() * 90000
        pepsi = self.main_ui.spinBox_3.value() * 40000
        return ve_gia, bap_mini, bap_lon, pepsi, ve_gia + bap_mini + bap_lon + pepsi

    def get_seat_names(self):
        return ", ".join(self.main_ui.selected_seats)

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.processor = PaymentProcessor(self)
        self.selected_seats = []
        self.selected_time = None
        self.selected_time_text = ""
        self.movies = self.load_movie_data("datatime.txt", "tomtat1.txt")
        self.doc_ghe_da_dat()
        self.thanh_toan_button.clicked.connect(self.show_payment_window)
        self.connect_seat_buttons()
        self.connect_time_buttons()
        self.connect_movie_labels()

        self.payment_ui = None
        self.payment_window = None
        self.qr_window = None
        self.qr_ui = None

    def luu_doanh_thu(self):
        ve_gia, bap_mini, bap_lon, pepsi, tong_tien = self.processor.calculate_total()
        try:
            with open("datadoanhthu.txt", "a", encoding="utf-8") as file:
                file.write(
                    f"{self.ten_phim_label.text()} | {tong_tien} | {self.spinBox.value()}, {self.spinBox_2.value()}, {self.spinBox_3.value()}\n")
            print("Đã lưu doanh thu vào file datadoanhthu.txt")
        except Exception as e:
            print("Lỗi lưu doanh thu:", e)

    def connect_seat_buttons(self):
        for row in "ABCDEF":
            for col in "123456":
                btn = self.findChild(QPushButton, f"{row}{col}")
                if btn:
                    btn.clicked.connect(lambda checked, b=btn: self.select_seat(b))

    def select_seat(self, button):
        seat = button.text()
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            button.setStyleSheet("background-color: rgb(255, 170, 255);")
        else:
            self.selected_seats.append(seat)
            button.setStyleSheet("background-color: #ff41fc;")


    def connect_time_buttons(self):
        times = [self.eight, self.halfpastten, self.twelve, self.halfpastthree, self.sixpm, self.halfpastseven]
        for btn in times:
            btn.clicked.connect(lambda checked, b=btn: self.select_time(b))

    def select_time(self, button):
        self.selected_seats.clear()  # Reset danh sách ghế đã chọn mỗi khi chọn suất chiếu mới
        self.reset_ghe()
        if self.selected_time:
            self.selected_time.setStyleSheet("background-color: rgb(241, 160, 255);")
        self.selected_time = button
        button.setStyleSheet("background-color: purple;")
        self.selected_time_text = button.text()
        print(f"Đã chọn suất chiếu: {self.selected_time_text}")
        self.doc_ghe_da_dat()  # Gọi đọc file sau khi reset ghế
        self.doc_ghe_da_dat()  # Gọi đọc file sau khi reset ghế

    def connect_movie_labels(self):
        for movie in self.movies.keys():
            label = self.findChild(QLabel, self.get_movie_id(movie))
            if label:
                label.mousePressEvent = lambda event, t=movie: self.show_movie_info(t)

    def show_movie_info(self, movie):
        self.movies = self.load_movie_data("datatime.txt", "tomtat1.txt")
        print("Dữ liệu đã được làm mới")
        self.reset_ghe()
        self.selected_seats.clear()
        info = self.movies[movie]
        self.ten_phim_label.setText(movie)
        self.the_loai_phim_label.setText(info[0])
        self.thoi_luong_phim_label.setText(info[1])
        self.mo_ta_phim_label.setWordWrap(True)
        self.mo_ta_phim_label.setText(info[2])  # Thêm dòng này
        self.doc_ghe_da_dat()

    def load_movie_data(self, file_time, file_mota):
        movies = {}
        try:
            with open(file_time, "r", encoding="utf-8") as file_time, open(file_mota, "r", encoding="utf-8") as file_mota:
                lines_time = [line.strip() for line in file_time.readlines() if line.strip()]
                lines_mota = [line.strip() for line in file_mota.readlines() if line.strip()]



                
            for time, mota in zip(lines_time, lines_mota):
                parts = time.strip().split(" | ")
                if len(parts) == 3:
                    ten, the_loai, thoi_luong = parts
                    mo_ta = mota.strip()
                    movies[ten] = (the_loai, thoi_luong, mo_ta)
        except FileNotFoundError:
                print("Không tìm thấy file dữ liệu")
        return movies
            
            
    def get_movie_id(self, movie_name):
        return {
            "Avatar": "phim1",
            "Barbie": "phim2",
            "A Man Called Otto": "phim3",
            "Past lives": "phim4",
            "The Creator": "phim5",
            "Guardians of the Galaxy": "phim6",
            "Ant-Man and The Wasp": "phim7",
        }.get(movie_name, "")

    def show_payment_window(self):
        if not self.selected_seats:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ghế!")
            return
        if not self.selected_time:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn suất chiếu!")
            return

        self.setDisabled(True)

        self.payment_window = QMainWindow()
        self.payment_ui = HoaDonWindow()
        self.payment_ui.setupUi(self.payment_window)

        self.payment_ui.label_Film.setText(self.ten_phim_label.text())
        self.payment_ui.label_Suatchiu.setText(self.selected_time.text())
        self.payment_ui.label_chair.setText(self.processor.get_seat_names())

        ve_gia, bap_mini, bap_lon, pepsi, tong_tien = self.processor.calculate_total()

        self.payment_ui.label_veticket.setText(str(len(self.selected_seats)))
        self.payment_ui.label_tongticket.setText(f"{ve_gia} VNĐ")
        self.payment_ui.label_cornmini.setText(str(self.spinBox.value()))
        self.payment_ui.label_tongcornmini.setText(f"{bap_mini} VNĐ")
        self.payment_ui.label_cornbig.setText(str(self.spinBox_2.value()))
        self.payment_ui.label_tongcornbig.setText(f"{bap_lon} VNĐ")
        self.payment_ui.label_pepsi.setText(str(self.spinBox_3.value()))
        self.payment_ui.label_tongpepsi.setText(f"{pepsi} VNĐ")
        self.payment_ui.label_tongall.setText(f"{tong_tien} VNĐ")

        # Liên kết sự kiện cho các nút trên giao diện hóa đơn từ file nutthanhtoan.py
        setup_hoadon_button_links(self.payment_ui, self)
        # Liên kết nút thanh toán tiền mặt với phương thức show_cash_payment
        self.payment_ui.pushButton_tienmat.clicked.connect(self.show_cash_payment)

        self.payment_window.show()

    def show_qr_payment(self):

        self.payment_window.hide()
        self.qr_window = QMainWindow()
        self.qr_ui = Ui_QRWindow()
        self.qr_ui.setupUi(self.qr_window)

        self.qr_ui.ButtonXacnhanTT.clicked.connect(self.qr_payment_success)
        self.qr_ui.ButtonQuaylaiTT.clicked.connect(lambda: (self.qr_window.close(), self.payment_window.show()))

        self.qr_window.show()

    def qr_payment_success(self):
        QMessageBox.information(self, "Thanh toán", "Thanh toán thành công!")
        self.luu_ghe_da_dat()
        self.luu_doanh_thu()
        self.doc_ghe_da_dat()
        self.doc_doanh_thu()
        self.qr_window.close()
        self.payment_window.close()
        self.setDisabled(False)
        self.selected_seats.clear()
        self.reset_ghe()

    def show_cash_payment(self):
        QMessageBox.information(self, "Thanh toán", "Đặt vé thành công. Vui lòng thanh toán & nhận vé tại quầy!")
        self.luu_ghe_da_dat()
        self.luu_doanh_thu()
        self.doc_ghe_da_dat()
        self.doc_doanh_thu()
        self.payment_window.close()
        self.setDisabled(False)
        self.selected_seats.clear()
        self.reset_ghe()

    def luu_ghe_da_dat(self):
        try:
            with open("dataghe.txt", "a", encoding="utf-8") as file:
                for seat in self.selected_seats:
                    file.write(f"{self.ten_phim_label.text()} | {self.selected_time_text} | {seat}\n")
                    print("Đã lưu dữ liệu vào file dataghe.txt")
        except Exception as e:
            print("Lỗi lưu ghế:", e)

    def doc_ghe_da_dat(self):
        try:
            print(f"Đang đọc file cho phim: {self.ten_phim_label.text()} | Giờ: {self.selected_time_text}")
            with open("dataghe.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(" | ")
                    if len(parts) == 3:
                        ten_phim, gio_chieu, ghe = parts
                        if (ten_phim.strip() == self.ten_phim_label.text().strip() and
                                gio_chieu.strip() == self.selected_time_text.strip()):
                            btn = self.findChild(QPushButton, ghe)
                            if btn:
                                btn.setStyleSheet("background-color: rgb(58, 79, 130);")  # Xanh đã đặt
                                btn.setDisabled(True)  # Khóa ghế
                                print(f"Khóa ghế {ghe} thành công!")
        except FileNotFoundError:
            print("File không tồn tại")
        except Exception as e:
            print(f"Lỗi đọc file: {e}")

    def reset_ghe(self):
        try:
            self.selected_seats.clear()  # Clear ban đầu
            # Reset màu tất cả ghế về hồng
            for button in self.centralwidget.findChildren(QPushButton):
                if button.objectName() and len(button.objectName()) == 2:
                    button.setStyleSheet("background-color: rgb(255, 170, 255);")  # Hồng ban đầu
                    button.setEnabled(True)

            # Đọc lại file ghế đã đặt
            with open("dataghe.txt", "r", encoding="utf-8") as file:
                ghe_da_dat = [line.strip().split(" | ") for line in file.readlines()]

            # Reset ghế nào đã đặt (màu xanh + khóa)
            for item in ghe_da_dat:
                if len(item) == 3:  # Chỉ xử lý dòng đủ 3 phần
                    ten_phim, gio_chieu, ghe = item
                    if ten_phim == self.ten_phim_label.text() and gio_chieu == self.selected_time_text:
                        btn = self.findChild(QPushButton, ghe)
                        if btn:
                            btn.setStyleSheet("background-color: rgb(58, 79, 130);")  # Màu xanh đã đặt
                            btn.setDisabled(True)

        except FileNotFoundError:
            print("File không tồn tại")
        except Exception as e:
            print(f"lỗi reset ghế:{e}")


    def luu_doanh_thu(self):
        ve_gia, bap_mini, bap_lon, pepsi, tong_tien = self.processor.calculate_total()
        try:
            file_path = os.path.join(os.getcwd(), "datadoanhthu.txt")
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(f"{self.ten_phim_label.text()} | {len(self.selected_seats)} | {tong_tien} | {self.spinBox.value()}, {self.spinBox_2.value()}, {self.spinBox_3.value()}\n")
            print("Đã lưu doanh thu vào file datadoanhthu.txt")
        except Exception as e:
            print("Lỗi lưu doanh thu:", {e})

    def doc_doanh_thu(self):
        try:
            print("Đang đọc dữ liệu doanh thu...")
            with open("datadoanhthu.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    print(line.strip())  # In dữ liệu doanh thu để kiểm tra
        except FileNotFoundError:
            print("File doanh thu không tồn tại")
        except Exception as e:
            print(f"Lỗi đọc file doanh thu: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())

import sys
import sqlite3
import pandas as pd
import os

sys.path.append(os.path.abspath("Managementlogin"))
sys.path.append(os.path.abspath("Managementwindow"))

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog
from PyQt6 import QtWidgets
from Managementlogin.mainwd import Ui_MainWindow as MainUI
from Managementlogin.dangnhapusers import Ui_MainWindow as LoginUI
from Managementlogin.dangky import Ui_MainWindow as SignupUI
from Managementlogin.dangnhapadmin import  Ui_MainWindow as AdminloginUi
from Managementwindow.giaodienmodau import Ui_MainWindow  # Giao diện chính
from Managementwindow.giaodienchucnangnhanvien import Ui_EmployeeWindow  # Giao diện nhân viên
from Managementwindow.giaodienchucnangdoanhthu import Ui_RevenueWindow  # Giao diện báo cáo doanh thu
from Managementwindow.MainWindow import Ui_MainWindow as QuanlyUI

def initialize_database():
    conn = sqlite3.connect("dulieuchucnang.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS new_employees (
            name TEXT,
            birthdate TEXT,
            position TEXT,
            email TEXT,
            phone TEXT,
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS new_revenue (
            name TEXT,
            tickets_sold INTEGER,
            revenue REAL,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


class giaodientong(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_ui = MainUI()
        self.main_ui.setupUi(self)

        self.login_window = giaodiendangnhap(self)  # Khởi tạo cửa sổ đăng nhập
        self.adminlogin_window = giaodiendangnhapadmin(self)
        #  khi nhấn nút "users" mở cửa sổ đăng nhập
        self.main_ui.Users.clicked.connect(self.open_login)
        self.main_ui.Admin.clicked.connect(self.open_adminlogin)
    def open_login(self):
        self.hide()  # Ẩn giao diện chính
        self.login_window.show()  # Hiển thị giao diện đăng nhập

    def open_adminlogin(self):
            self.hide()  # Ẩn giao diện chính
            self.adminlogin_window.show()  # Hiển thị giao diện đăng nhập
class giaodiendangnhapadmin (QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.adminlogin_ui = AdminloginUi()
        self.adminlogin_ui.setupUi(self)
        self.adminlogin_ui.back.clicked.connect(self.back_to_main)
    def back_to_main(self):
        self.main_window = giaodientong()
        self.main_window.show()
        self.close()
class giaodiendangnhap(QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.login_ui = LoginUI()
        self.login_ui.setupUi(self)
        self.signup_window = giaodiendangky(self)  # khởi tạo cửa sổ đăng ký
        self.login_ui.back.clicked.connect(self.back_to_main)
        # khi ấn signup thì chuyển sang cửa sổ đăng ký
        self.login_ui.dangky.clicked.connect(self.open_signup)
    def open_signup(self):
            self.hide()# tương tự với trên dùng để ẩn cửa sộ
            self.signup_window.show()
    def back_to_main(self):
        self.main_window = giaodientong()
        self.main_window.show()
        self.close()

class giaodiendangky(QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.signup_ui = SignupUI()
        self.signup_ui.setupUi(self)
        self.main_window = main_window  # Lưu tham chiếu tới cửa sổ chính


# Giao diện chính
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút chức năng
        self.ui.ButtonNhanVien.clicked.connect(self.open_employee_window)
        self.ui.ButtonDoanhthu.clicked.connect(self.open_revenue_window)
        self.ui.ButtonChung.clicked.connect(self.open_quanlychung)
        self.ui.ButtonDangxuat.clicked.connect(self.logout)
    def logout(self):
        self.close()

    def open_employee_window(self):
        self.employee_window = EmployeeWindow()
        self.employee_window.show()
        self.hide()
    def open_quanlychung(self):
        self.quanly_window=quanlywindow()
        self.quanly_window.show()
        self.hide()
    def open_revenue_window(self):
        try:
            self.revenue_window = RevenueWindow()
            self.revenue_window.show()
            self.hide()
        except Exception as e:
            print(f"Lỗi khi mở giao diện doanh thu: {e}")

class quanlywindow(QMainWindow):
    def __init__(self):
        super(quanlywindow, self).__init__()
        self.ui = QuanlyUI()
        self.ui.setupUi(self)
        self.ui.ButtonQuaylaiDT.clicked.connect(self.back_to_main)
    def back_to_main(self):
        self.main_window = giaodientong()
        self.main_window.show()
        self.close()

# Giao diện nhân viên
class EmployeeWindow(QMainWindow):
    def __init__(self):
        super(EmployeeWindow, self).__init__()
        self.ui = Ui_EmployeeWindow()
        self.ui.setupUi(self)

        # Kết nối các nút chức năng
        self.ui.ButtonQuaylaiNV.clicked.connect(self.back_to_main)
        self.ui.ButtonXoaNV.clicked.connect(self.delete_employee)
        self.ui.ButtonTaiNV.clicked.connect(self.download_employee)
        self.ui.ButtonLuuNV.clicked.connect(self.save_employee_data)

        # Load dữ liệu
        self.load_employee_data()

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def delete_employee(self):
        selected_item = self.ui.tableWidget.currentItem()
        if selected_item:
            selected_item.setText("")
            QMessageBox.information(self, "Xóa", "Ô đã được xoá!")
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một ô để xóa!")

    def download_employee(self):
        path, _ = QFileDialog.getSaveFileName(self, "Lưu file", "Nhanvien.xlsx", "Excel Files (*.xlsx)")
        if path:
            data = []
            for row in range(self.ui.tableWidget.rowCount()):
                row_data = []
                for col in range(self.ui.tableWidget.columnCount()):
                    item = self.ui.tableWidget.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            df = pd.DataFrame(data, columns=[self.ui.tableWidget.horizontalHeaderItem(i).text() for i in
                                             range(self.ui.tableWidget.columnCount())])
            df.to_excel(path, index=False)
            QMessageBox.information(self, "Thành công", "Dữ liệu nhân viên đã được lưu!")

    def save_employee_data(self):
        conn = sqlite3.connect("dulieuchucnang.db")
        cursor = conn.cursor()

        # Xóa dữ liệu cũ trong bảng new_employees để không lưu chồng dữ liệu
        cursor.execute("DELETE FROM new_employees")

        row_count = self.ui.tableWidget.rowCount()
        col_count = self.ui.tableWidget.columnCount()

        # Lưu dữ liệu từ giao diện vào database
        for row in range(row_count):
            values = []
            is_empty_row = True  # Dùng để kiểm tra nếu dòng này có dữ liệu hay không

            for col in range(col_count):  # Lặp qua tất cả các cột
                item = self.ui.tableWidget.item(row, col)
                text_value = item.text().strip() if item else ""  # Nếu ô trống thì gán giá trị là ""
                values.append(text_value)

                if text_value:  # Nếu ô có dữ liệu, dòng này không còn trống
                    is_empty_row = False

            if not is_empty_row:
                try:
                    # Đảm bảo có đủ 7 giá trị, nếu không thì thêm giá trị trống vào
                    while len(values) < 7:
                        values.append("")  # Thêm giá trị rỗng vào nếu thiếu

                    # Chèn dữ liệu vào bảng new_employees
                    cursor.execute("""
                        INSERT INTO new_employees (name, birthdate, position, email, phone, username, password)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, values)

                except sqlite3.Error as e:
                    print(f"Lỗi khi lưu dữ liệu nhân viên: {e}")

        conn.commit()
        conn.close()

        # Thông báo khi lưu thành công
        QMessageBox.information(self, "Thành công", "Dữ liệu đã được lưu!")

    def load_employee_data(self):
        conn = sqlite3.connect("dulieuchucnang.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM new_employees")
        records = cursor.fetchall()
        conn.close()

        # Giữ nguyên số dòng ban đầu trong giao diện
        row_count = self.ui.tableWidget.rowCount()

        # Nếu có dữ liệu từ cơ sở dữ liệu
        for row_idx in range(row_count):
            for col_idx in range(self.ui.tableWidget.columnCount()):
                # Kiểm tra nếu có dữ liệu từ database, cập nhật ô đó
                if row_idx < len(records) and col_idx < len(records[row_idx]):
                    value = records[row_idx][col_idx]
                    self.ui.tableWidget.setItem(row_idx, col_idx,
                                                QTableWidgetItem(str(value) if value is not None else ""))
                else:
                    # Nếu không có dữ liệu từ cơ sở dữ liệu, giữ ô trống
                    self.ui.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(""))


# Giao diện báo cáo doanh thu
class RevenueWindow(QMainWindow):
    def __init__(self):
        super(RevenueWindow, self).__init__()
        self.ui = Ui_RevenueWindow()
        self.ui.setupUi(self)
        self.file_path = "datadoanhthu.txt"
        self.load_revenue_data()

        # Kết nối các nút chức năng
        self.ui.ButtonQuaylaiDT.clicked.connect(self.back_to_main)
        self.ui.ButtonXoaDT.clicked.connect(self.delete_revenue_data)
        self.ui.ButtonTaiDT.clicked.connect(self.load_revenue_data)
        self.ui.ButtonLuuDT.clicked.connect(self.save_revenue_data)

    def back_to_main(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def delete_revenue_data(self):
        selected_item = self.ui.tableWidget_2.currentItem()
        if selected_item:
            selected_item.setText("")
            QMessageBox.information(self.ui, "Xóa", "Ô đã được xoá!")
        else:
            QMessageBox.warning(self.ui, "Lỗi", "Vui lòng chọn một ô để xóa!")

    def save_revenue_data(self):
        # row_count = self.ui.tableWidget_2.rowCount()
        # col_count = self.ui.tableWidget_2.columnCount()
        #
        # data = []
        # for row in range(row_count):
        #     row_data = []
        #     for col in range(col_count):
        #         item = self.ui.tableWidget_2.item(row, col)
        #         row_data.append(item.text().strip() if item else "")
        #     data.append(row_data)
        #
        # try:
        #     with open(self.file_path, "w", newline="", encoding="utf-8") as file:
        #         writer = csv.writer(file)
        #         writer.writerows(data)
        #     QMessageBox.information(self.ui, "Thành công", "Dữ liệu đã được lưu!")
        # except Exception as e:
        #     QMessageBox.warning(self.ui, "Lỗi", f"Không thể lưu dữ liệu: {str(e)}")

            try:
                with open("datadoanhthu.txt", "w", encoding="utf-8") as file:
                    row_count = self.ui.tableWidget_2.rowCount()
                    col_count = self.ui.tableWidget_2.columnCount()

                    for row in range(row_count):
                        values = []
                        for col in range(col_count):
                            item = self.ui.tableWidget_2.item(row, col)
                            text_value = item.text().strip() if item else ""  # Nếu ô trống, thay bằng chuỗi rỗng
                            values.append(text_value)

                        # Ghép các giá trị với dấu " | " để giữ đúng định dạng ban đầu
                        file.write(" | ".join(values) + "\n")

                QMessageBox.information(self, "Thành công", "Dữ liệu đã được lưu!")

            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu dữ liệu: {str(e)}")

    def load_revenue_data(self):
        try:
            with open("datadoanhthu.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

            self.ui.tableWidget_2.setRowCount(len(lines))  # Đặt số dòng theo file
            self.ui.tableWidget_2.setColumnCount(4)  # Đảm bảo có đủ 4 cột

            for row_idx, line in enumerate(lines):
                columns = line.strip().split("|")  # Chia dữ liệu theo dấu "|"

                # Đảm bảo danh sách columns có đủ 4 phần tử
                while len(columns) < 4:
                    columns.append("")

                # Thêm dữ liệu vào bảng
                self.ui.tableWidget_2.setItem(row_idx, 0, QTableWidgetItem(columns[0].strip()))  # Tên phim
                self.ui.tableWidget_2.setItem(row_idx, 1, QTableWidgetItem(columns[1].strip()))  # Số vé đã bán
                self.ui.tableWidget_2.setItem(row_idx, 2, QTableWidgetItem(columns[2].strip()))  # Thành tiền
                self.ui.tableWidget_2.setItem(row_idx, 3, QTableWidgetItem(columns[3].strip()))  # Ghi chú

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu doanh thu: {str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = giaodientong()
    main_window.show()
    sys.exit(app.exec())

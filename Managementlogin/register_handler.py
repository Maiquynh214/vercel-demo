import sqlite3
import re
from PyQt6.QtWidgets import QMessageBox
from PyQt6.uic.properties import QtWidgets


# Kết nối hoặc tạo database
def create_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def suggest_username(ui):
        """ Tự động đề xuất tên đăng nhập dựa trên email. """
        email = ui.lineEdit_email.text()
        if "@" in email:
            ui.lineEdit_dnhap.setText(email.split("@")[0])

# Kiểm tra email hợp lệ
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

# Kiểm tra số điện thoại hợp lệ
def is_valid_phone(phone):
    return re.match(r"^\d{10,11}$", phone)

# Xử lý đăng ký
def register(username, email, phone, password, confirm_password, window):
    if not username or not email or not phone or not password or not confirm_password:
        QMessageBox.warning(window, " Kiểm tra", "Vui lòng nhập đầy đủ thông tin!")
        return

    if not is_valid_email(email):
        QMessageBox.warning(window, " Kiểm tra", "Email không hợp lệ!")
        return

    if not is_valid_phone(phone):
        QMessageBox.warning(window, "Kiểm tra", "Số điện thoại không hợp lệ!")
        return

    if password != confirm_password:
        QMessageBox.warning(window, "Kiểm tra", "Mật khẩu nhập lại không khớp!")
        return

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, phone, password) VALUES (?, ?, ?, ?)",
                       (username, email, phone, password))
        conn.commit()
        conn.close()
        QMessageBox.information(window, "Thành công", "Đăng ký thành công!")
    except sqlite3.IntegrityError:
        QMessageBox.warning(window, "Kiểm tra", "Tên đăng nhập, email hoặc số điện thoại đã tồn tại!")

"""" xử lý giao diện đăng nhập """


def check_login(username, password):
    connection = sqlite3.connect("users.db")  #  Kết nối database SQLite
    cursor = connection.cursor()
    connection.commit()

    # Kiểm tra tài khoản trong database
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()


    connection.close()
    return user is not None
"""XỬ LÝ CỦA GIAO DIỆN ADMIN"""


def kiemtraadmin(username, password):
    try:
        with open("listquanly.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines[1:]:  # Bỏ qua dòng tiêu đề
                parts = line.strip().split(" | ")
                if len(parts) >= 3:  # Kiểm tra định dạng dòng
                    stored_username, stored_password = parts[1], parts[2]
                    if username == stored_username and password == stored_password:
                        return True
    except FileNotFoundError:
        QtWidgets.QMessageBox.critical(None, "Lỗi", "Không tìm thấy file dữ liệu!")
    return None
  # Không tìm thấy trong file, tiếp tục kiểm tra D
def kiemtra_trong_db(username, password):
            try:
                conn = sqlite3.connect("dulieuchucnang.db")  # Đảm bảo đúng đường dẫn file
                cursor = conn.cursor()
                query = "SELECT * FROM new_employees WHERE username = ? AND password = ?"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()  # Nếu tìm thấy tài khoản, trả về True
                conn.close()
                return result is not None
            except sqlite3.Error as e:
                print("Lỗi truy vấn database:", e)
                return False

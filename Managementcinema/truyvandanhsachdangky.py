import sqlite3
from PyQt6 import QtWidgets


def truyvannguoidangky():
    connection = sqlite3.connect("users.db")  # Kết nối database
    cursor = connection.cursor()

    # Truy vấn danh sách người dùng theo thứ tự đăng ký
    cursor.execute("SELECT id, username, email, phone, password FROM users ORDER BY id ASC")
    users = cursor.fetchall()  # Lấy toàn bộ kết quả

    connection.close()
    return users  # Trả về danh sách [(id, username, email, phone, password), ...]


def dulieunguoidangky():
    users = truyvannguoidangky()  # Lấy danh sách từ database

    if not users:
        QtWidgets.QMessageBox.information(None, "Danh sách", "Chưa có ai đăng ký!")
        return

    # Tạo chuỗi danh sách
    user_list = "\n".join(
        [f"{id}. {username} - {email} - {phone} - {password}" for id, username, email, phone, password in users])

    # Hiển thị danh sách trong hộp thoại
    QtWidgets.QMessageBox.information(None, "Danh sách người dùng", user_list)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dulieunguoidangky()
    sys.exit(app.exec())

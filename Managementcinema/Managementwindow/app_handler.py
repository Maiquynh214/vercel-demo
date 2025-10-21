
import sqlite3  # Thư viện làm việc với SQLite
from PyQt6 import QtWidgets
import os
import sqlite3

# Lấy đường dẫn thư mục "Quản lý vé xem phim"
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Đường dẫn đầy đủ đến file users.db
DATABASE_PATH = os.path.join(project_root, "users.db")

# Kiểm tra xem file database có tồn tại không
if not os.path.exists(DATABASE_PATH):
    print(f"❌ Lỗi: Không tìm thấy database tại {DATABASE_PATH}")
else:
    print(f"✅ Database được tìm thấy tại {DATABASE_PATH}")

# Kết nối database
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# ==========================
# 🔹 PHẦN XỬ LÝ DATABASE 🔹
# ==========================
def get_db_connection():
    """Tạo và trả về một kết nối đến cơ sở dữ liệu SQLite."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Giúp truy xuất dữ liệu dạng từ điển
    return conn


def get_all_users():
    """Lấy danh sách tất cả người dùng từ bảng users."""
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("SELECT id, username, email FROM users")
    # users = cursor.fetchall()
    # conn.close()
    # return [dict(user) for user in users]  # Chuyển thành danh sách dictionary
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, phone FROM users")  # Lấy thêm số điện thoại
    users = cursor.fetchall()
    conn.close()
    return users

def add_user(username: str, email: str):
    """Thêm một người dùng mới vào database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    conn.commit()
    conn.close()


def delete_user(user_id: int):
    """Xóa một người dùng dựa trên ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    print(f"✅ Đã xoá người dùng ID {user_id} khỏi database")


def update_user(user_id: int, username: str, email: str, phone: str):
    """Cập nhật thông tin người dùng trong database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, email = ?, phone = ? WHERE id = ?",
                   (username, email, phone, user_id))
    conn.commit()
    conn.close()
    print(f"✅ Đã cập nhật thông tin cho người dùng ID {user_id}")


# ==========================
# 🔹 PHẦN XỬ LÝ GIAO DIỆN 🔹
# ==========================
def load_users(main_window):
    """Hiển thị danh sách người dùng trong MainWindow.py"""
    users = get_all_users()
    main_window.tableWidget_3.setRowCount(len(users))  # Cập nhật số hàng

    for row, user in enumerate(users):
        try:
            main_window.tableWidget_3.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))  # ID
            main_window.tableWidget_3.setItem(row, 1, QtWidgets.QTableWidgetItem(user[1]))  # Username
            main_window.tableWidget_3.setItem(row, 2, QtWidgets.QTableWidgetItem(user[2]))  # Email
            main_window.tableWidget_3.setItem(row, 3, QtWidgets.QTableWidgetItem(user[3]))  # Phone
        except Exception as e:
            print(f"❌ Lỗi cập nhật bảng tại hàng {row}: {e}")
def edit_user(ui):
    """Xử lý sự kiện chỉnh sửa người dùng."""
    selected_row = ui.tableWidget_3.currentRow()
    if selected_row < 0:
        QtWidgets.QMessageBox.warning(None, "Lỗi", "Vui lòng chọn một người dùng để chỉnh sửa.")
        return

    user_id = ui.tableWidget_3.item(selected_row, 0).text()  # ID người dùng
    username = ui.tableWidget_3.item(selected_row, 1).text()
    email = ui.tableWidget_3.item(selected_row, 2).text()
    phone = ui.tableWidget_3.item(selected_row, 3).text()

    new_username, ok0 = QtWidgets.QInputDialog.getText(None, "Chỉnh sửa", "Nhập tên mới:", text=username)
    new_email, ok1 = QtWidgets.QInputDialog.getText(None, "Chỉnh sửa", "Nhập email mới:", text=email)
    new_phone, ok2 = QtWidgets.QInputDialog.getText(None, "Chỉnh sửa", "Nhập sđt mới:", text=phone)

    if ok0 and ok1 and ok2:
        update_user(user_id, new_username, new_email, new_phone)  # Truyền đúng user_id
        load_users(ui)  # Cập nhật lại danh sách sau khi chỉnh sửa

def delete_user_event(ui):
    """Xử lý sự kiện xoá người dùng."""
    selected_row = ui.tableWidget_3.currentRow()
    if selected_row < 0:
        QtWidgets.QMessageBox.warning(None, "Lỗi", "Vui lòng chọn một người dùng để xoá.")
        return

    user_id = ui.tableWidget_3.item(selected_row, 0).text()  # Lấy ID người dùng
    confirm = QtWidgets.QMessageBox.question(None, "Xác nhận",
                                             f"Bạn có chắc muốn xoá người dùng ID {user_id}?",
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    if confirm == QtWidgets.QMessageBox.Yes:
        delete_user(user_id)  # Xoá người dùng theo ID
        load_users(ui)  # Cập nhật lại danh sách
        print(f"✅ Đã xoá người dùng ID {user_id}")


# event_handlers.py
def setup_hoadon_button_links(payment_ui, main_app):
    # Liên kết nút thanh toán bằng QR với hàm xử lý của main_app
    payment_ui.pushButton_QR.clicked.connect(main_app.show_qr_payment)
    # Nếu cần, liên kết các nút khác (ví dụ: thanh toán tiền mặt)
    # payment_ui.pushButton_tienmat.clicked.connect(main_app.show_cash_payment)

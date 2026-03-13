import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.connection import init_connection_pool


def main():

    try:
        init_connection_pool()
        print("Подключение к базе данных успешно установлено")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        print("Проверьте параметры подключения в database/connection.py")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
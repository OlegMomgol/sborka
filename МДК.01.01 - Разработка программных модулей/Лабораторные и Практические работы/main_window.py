import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QLabel,
    QMessageBox, QHeaderView, QDialog, QDialogButtonBox,
    QFormLayout, QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QAction

from services.note_service import NoteService


class NoteDialog(QDialog):
  

    def __init__(self, service, categories, users, note=None, parent=None):
        super().__init__(parent)
        self.service = service
        self.note = note
        self.categories = categories
        self.users = users

        self.setWindowTitle("Новая заметка" if not note else "Редактирование заметки")
        self.setModal(True)
        self.resize(500, 400)

        self.setup_ui()

        if note:
            self.load_note_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Введите заголовок")
        form_layout.addRow("Заголовок:", self.title_edit)

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Введите текст заметки")
        form_layout.addRow("Содержание:", self.content_edit)

        self.category_combo = QComboBox()
        for category in self.categories:
            self.category_combo.addItem(category.name, category.id)
        form_layout.addRow("Категория:", self.category_combo)

        self.user_combo = QComboBox()
        for user in self.users:
            self.user_combo.addItem(user.username, user.id)

        if not self.note:
            form_layout.addRow("Пользователь:", self.user_combo)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def load_note_data(self):
        self.title_edit.setText(self.note.title)
        self.content_edit.setText(self.note.content)

        index = self.category_combo.findData(self.note.category_id)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)

    def get_data(self):
        return {
            'title': self.title_edit.text(),
            'content': self.content_edit.toPlainText(),
            'category_id': self.category_combo.currentData(),
            'user_id': self.user_combo.currentData() if not self.note else None
        }


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.service = NoteService()
        self.current_user_id = 1

        self.setWindowTitle("Note Manager")
        self.setMinimumSize(900, 600)

        self.setup_ui()
        self.load_data()
        self.load_categories_to_filter()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        toolbar = self.addToolBar("Главная")

        add_action = QAction("➕ Добавить", self)
        add_action.triggered.connect(self.add_note)
        toolbar.addAction(add_action)

        refresh_action = QAction("🔄 Обновить", self)
        refresh_action.triggered.connect(self.load_data)
        toolbar.addAction(refresh_action)

        toolbar.addSeparator()

        search_filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию...")
        self.search_input.textChanged.connect(self.search_notes)
        search_filter_layout.addWidget(self.search_input, 2)

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все категории", None)
        self.filter_combo.currentIndexChanged.connect(self.filter_notes)
        search_filter_layout.addWidget(self.filter_combo, 1)

        main_layout.addLayout(search_filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Заголовок", "Категория", "Пользователь", "Дата создания"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_note)

        main_layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_note)
        button_layout.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_note)
        button_layout.addWidget(self.delete_btn)

        self.view_btn = QPushButton("Просмотр")
        self.view_btn.clicked.connect(self.view_note)
        button_layout.addWidget(self.view_btn)

        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def load_categories_to_filter(self):
        try:
            categories = self.service.get_all_categories()
            for category in categories:
                self.filter_combo.addItem(category.name, category.id)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить категории: {e}")

    def load_data(self):
        try:
            notes = self.service.get_all_notes()
            self.display_notes(notes)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить заметки: {e}")

    def display_notes(self, notes):
        self.table.setRowCount(len(notes))

        for row, note in enumerate(notes):
            self.table.setItem(row, 0, QTableWidgetItem(str(note.id)))
            self.table.setItem(row, 1, QTableWidgetItem(note.title))

            category_name = ""
            if hasattr(note, 'category_name') and note.category_name:
                category_name = note.category_name
            self.table.setItem(row, 2, QTableWidgetItem(category_name))

            username = ""
            if hasattr(note, 'username') and note.username:
                username = note.username
            self.table.setItem(row, 3, QTableWidgetItem(username))

            created_at = ""
            if note.created_at:
                created_at = note.created_at.strftime("%d.%m.%Y %H:%M")
            self.table.setItem(row, 4, QTableWidgetItem(created_at))

        self.table.setColumnHidden(0, True)

    def search_notes(self):
        search_term = self.search_input.text()
        try:
            notes = self.service.search_notes(search_term)
            self.display_notes(notes)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при поиске: {e}")

    def filter_notes(self):
        category_id = self.filter_combo.currentData()
        try:
            notes = self.service.filter_notes_by_category(category_id)
            self.display_notes(notes)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при фильтрации: {e}")

    def add_note(self):
        try:
            categories = self.service.get_all_categories()
            users = self.service.get_all_users()

            if not categories:
                QMessageBox.warning(self,
                                    "Нет доступных категорий. Сначала создайте категории в БД.")
                return

            if not users:
                QMessageBox.warning(self,
                                    "Нет доступных пользователей. Сначала создайте пользователей в БД.")
                return

            dialog = NoteDialog(self.service, categories, users, parent=self)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()

                user_id = data['user_id'] or self.current_user_id

                note_id = self.service.create_note(
                    data['title'],
                    data['content'],
                    data['category_id'],
                    user_id
                )

                if note_id:
                    QMessageBox.information(self, "Успех")
                    self.load_data()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось создать заметку")

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка валидации", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")

    def get_selected_note_id(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return None

        row = selected_rows[0].row()
        return int(self.table.item(row, 0).text())

    def edit_note(self):
        note_id = self.get_selected_note_id()
        if not note_id:
            QMessageBox.warning(self, "Предупреждение", "Выберите заметку для редактирования")
            return

        try:
            note = self.service.get_note_by_id(note_id)
            if not note:
                QMessageBox.critical(self, "Ошибка", "Заметка не найдена")
                return

            categories = self.service.get_all_categories()

            dialog = NoteDialog(self.service, categories, [], note, self)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()

                success = self.service.update_note(
                    note_id,
                    data['title'],
                    data['content'],
                    data['category_id']
                )

                if success:
                    QMessageBox.information(self, "Успех", "Заметка успешно обновлена!")
                    self.load_data()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить заметку")

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка валидации", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")

    def delete_note(self):
        note_id = self.get_selected_note_id()
        if not note_id:
            QMessageBox.warning(self, "Предупреждение", "Выберите заметку для удаления")
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить эту заметку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.service.delete_note(note_id)

                if success:
                    QMessageBox.information(self, "Успех", "Заметка успешно удалена!")
                    self.load_data()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось удалить заметку")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")

    def view_note(self):
        note_id = self.get_selected_note_id()
        if not note_id:
            QMessageBox.warning(self, "Предупреждение", "Выберите заметку для просмотра")
            return

        try:
            note = self.service.get_note_by_id(note_id)
            if note:
                QMessageBox.information(
                    self,
                    note.title,
                    f"Содержание:\n\n{note.content}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")
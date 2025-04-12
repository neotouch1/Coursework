from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QRadioButton, QPushButton


'''
Этот класс предназначен для отображения окна с выбором реализации DCT
Итоговый метод класса возвращает в переменную True или False, который
отправится в класс DCT2D.
'''
class DCTSettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор реализации DCT")

        layout = QVBoxLayout()

        self.lable = QLabel("Выберите реализацию DCT:")
        layout.addWidget(self.lable)

        self.radio_custom = QRadioButton("Собственная реализация")
        self.radio_library = QRadioButton("Библиотечная реализация")

        self.radio_library.setChecked(True)


        layout.addWidget(self.radio_library)
        layout.addWidget(self.radio_custom)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)



    def selected_option(self):
        if self.radio_custom.isChecked():
            return True # использовать собственную реализацию
        else:
            return False # использовать библиотечную реализацию
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QRadioButton, QPushButton, QSlider
from PyQt5.QtCore import Qt

'''
Этот класс предназначен для отображения окна с выбором уровня сжатия изображения
Метод get_value - возвращает значение, которое
отправится в класс QuantizeBlocks для изменения матриц квантования.
'''

class CompressionLevelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Задать уровень сжатия")

        layout = QVBoxLayout()

        self.label = QLabel("Выберите уровень сжатия:")
        layout.addWidget(self.label)

        # Создание радиокнопок для выбора уровня сжатия
        self.radio_2 = QRadioButton("Среднее сжатие")
        self.radio_5 = QRadioButton("Грубое сжатие")

        # Установка значения по умолчанию (первый вариант)
        self.radio_2.setChecked(True)

        layout.addWidget(self.radio_2)
        layout.addWidget(self.radio_5)

        # Кнопка подтверждения
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_value(self):
        # Возвращаем значение в зависимости от выбранной радиокнопки
        if self.radio_2.isChecked():
            return 2
        else:
            return 5
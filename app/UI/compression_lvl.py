from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QRadioButton, QPushButton, QSlider
from PyQt5.QtCore import Qt

'''
Этот класс предназначен для отображения окна с выбором уровня сжатия изображения
Метод get_value - возвращает значение в процентах, которое
отправится в класс QuantizeBlocks для изменения матриц квантования.
'''

class CompressionLevelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Задать уровень сжатия")

        layout = QVBoxLayout()

        self.lable = QLabel("Введите уровень сжатия в процентах:")
        layout.addWidget(self.lable)


        # Ползунок для выбора уровня сжатия
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(1, 100)  # Диапазон от 1 до 100
        self.slider.setValue(50)  # Значение по умолчанию (среднее)
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        # Метка с текущим значением ползунка
        self.value_label = QLabel(f"Уровень сжатия: {self.slider.value()}%", self)
        layout.addWidget(self.value_label)

        # Кнопка подтверждения
        self.btn_ok = QPushButton("ОК", self)
        self.btn_ok.clicked.connect(self.accept)  # Закрывает окно
        layout.addWidget(self.btn_ok)

        self.setLayout(layout)

    def update_label(self):
        # Обновление метки с текущим значением
        self.value_label.setText(f"Уровень сжатия: {self.slider.value()}%")

    def get_value(self):
        return self.slider.value()  # Возвращает значение слайдера
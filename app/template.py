import sys
import cv2
import numpy as np
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from dct import DCT2D
from image_preparation import ImagePreparation
from quantize_bloks import QuantizeBlocks
from zigzag_transform import ZigzagTransform
from rle import RleProcessing

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 1000, 800)

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        control_layout = QVBoxLayout()

        # Метка для изображения
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label, stretch=3)

        # Метки для размеров изображения
        self.label_size_before = QLabel("Размер до сжатия: - байт")
        self.label_size_after = QLabel("Размер после сжатия: - байт")
        self.label_processing_time = QLabel("Время обработки: - сек")

        control_layout.addWidget(self.label_size_before)
        control_layout.addWidget(self.label_size_after)
        control_layout.addWidget(self.label_processing_time)

        # Основные кнопки
        self.btn_open = QPushButton("Открыть изображение")
        self.btn_open.clicked.connect(self.open_image)
        control_layout.addWidget(self.btn_open)

        self.btn_process = QPushButton("Обработать изображение")
        self.btn_process.clicked.connect(self.process_image)
        self.btn_process.setEnabled(False)
        control_layout.addWidget(self.btn_process)

        self.btn_save = QPushButton("Сохранить изображение")
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        control_layout.addWidget(self.btn_save)

        # Кнопки для просмотра промежуточных шагов
        self.btn_show_dct = QPushButton("Показать DCT-коэффициенты")
        self.btn_show_dct.clicked.connect(self.show_dct)
        self.btn_show_dct.setEnabled(False)
        control_layout.addWidget(self.btn_show_dct)

        self.btn_show_quant = QPushButton("Показать квантованные блоки")
        self.btn_show_quant.clicked.connect(self.show_quantized_blocks)
        self.btn_show_quant.setEnabled(False)
        control_layout.addWidget(self.btn_show_quant)

        self.btn_show_zigzag = QPushButton("Показать зигзаг")
        self.btn_show_zigzag.clicked.connect(self.show_zigzag)
        self.btn_show_zigzag.setEnabled(False)
        control_layout.addWidget(self.btn_show_zigzag)

        self.btn_show_rle = QPushButton("Показать RLE-данные")
        self.btn_show_rle.clicked.connect(self.show_rle)
        self.btn_show_rle.setEnabled(False)
        control_layout.addWidget(self.btn_show_rle)

        main_layout.addLayout(control_layout, stretch=1)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Переменные для хранения промежуточных данных
        self.image_path = None
        self.dct_blocks = None
        self.quantized_blocks = None
        self.zigzag_blocks = None
        self.rle_data = None
        self.original_size = 0
        self.compressed_size = 0

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")
        if file_name:
            self.image_path = file_name
            self.show_image(self.image_path)
            self.original_size = self.get_file_size(self.image_path)
            self.label_size_before.setText(f"Размер до сжатия: {self.original_size} байт")
            self.btn_process.setEnabled(True)

    def show_image(self, path):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def process_image(self):
        start_time = time.time()

        pre_img = ImagePreparation(self.image_path)
        bloks = pre_img.split_into_bloks()

        res_dct = DCT2D()
        res_dct.apply_dct_to_blocks(bloks)
        self.dct_blocks = res_dct.dct_blocks

        quant_blocks = QuantizeBlocks()
        quant_blocks.quantize_dct_bloks(self.dct_blocks)
        self.quantized_blocks = quant_blocks.quantized_blocks

        zig_ex = ZigzagTransform()
        self.zigzag_blocks = zig_ex.z_transform_blocks(self.quantized_blocks)

        rle = RleProcessing()
        self.rle_data = rle.apply_rle_all_blocks(self.zigzag_blocks)

        self.compressed_size = sum(len(block) for row in self.rle_data for block in row)
        self.label_size_after.setText(f"Размер после сжатия: {self.compressed_size} байт")

        end_time = time.time()
        self.label_processing_time.setText(f"Время обработки: {end_time - start_time:.2f} сек")

        # Включаем кнопки для просмотра промежуточных шагов
        self.btn_show_dct.setEnabled(True)
        self.btn_show_quant.setEnabled(True)
        self.btn_show_zigzag.setEnabled(True)
        self.btn_show_rle.setEnabled(True)
        self.btn_save.setEnabled(True)

    def show_dct(self):
        plt.figure()
        plt.imshow(self.dct_blocks[0, 0], cmap='gray')
        plt.title("DCT Коэффициенты (Первый блок)")
        plt.colorbar()
        plt.show()

    def show_quantized_blocks(self):
        plt.figure()
        plt.imshow(self.quantized_blocks[0, 0], cmap='gray')
        plt.title("Квантованные блоки (Первый блок)")
        plt.colorbar()
        plt.show()

    def show_zigzag(self):
        print("Зигзаг блоков:", self.zigzag_blocks[0, 0, :, 2])

    def show_rle(self):
        print("RLE данные для первого блока:", self.rle_data[0][0])

    def save_image(self):
        pass  # Реализация сохранения

    def get_file_size(self, path):
        try:
            return os.path.getsize(path)
        except:
            return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
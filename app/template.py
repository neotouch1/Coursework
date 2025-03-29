import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
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
        layout = QVBoxLayout()

        # Метка для изображения
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # === Основные кнопки ===
        self.btn_open = QPushButton("Открыть изображение", self)
        self.btn_open.clicked.connect(self.open_image)
        layout.addWidget(self.btn_open)

        self.btn_process = QPushButton("Обработать изображение", self)
        self.btn_process.clicked.connect(self.process_image)
        self.btn_process.setEnabled(False)
        layout.addWidget(self.btn_process)

        self.btn_save = QPushButton("Сохранить изображение", self)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

        # === Кнопки для промежуточных шагов ===
        self.btn_show_dct = QPushButton("Показать DCT-коэффициенты", self)
        self.btn_show_dct.clicked.connect(self.show_dct)
        self.btn_show_dct.setEnabled(False)
        layout.addWidget(self.btn_show_dct)

        self.btn_show_quant = QPushButton("Показать квантованные блоки", self)
        self.btn_show_quant.clicked.connect(self.show_quantized_blocks)
        self.btn_show_quant.setEnabled(False)
        layout.addWidget(self.btn_show_quant)

        self.btn_show_zigzag = QPushButton("Показать зигзаг", self)
        self.btn_show_zigzag.clicked.connect(self.show_zigzag)
        self.btn_show_zigzag.setEnabled(False)
        layout.addWidget(self.btn_show_zigzag)

        self.btn_show_rle = QPushButton("Показать RLE-данные", self)
        self.btn_show_rle.clicked.connect(self.show_rle)
        self.btn_show_rle.setEnabled(False)
        layout.addWidget(self.btn_show_rle)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Переменные для хранения промежуточных данных
        self.image_path = None
        self.processed_image = None
        self.dct_blocks = None
        self.quantized_blocks = None
        self.zigzag_blocks = None
        self.rle_data = None

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")
        if file_name:
            self.image_path = file_name
            self.show_image(self.image_path)
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
        if self.processed_image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "",
                                                       "PNG Files (*.png);;JPEG Files (*.jpg)")
            if file_name:
                cv2.imwrite(file_name, self.processed_image)
                print(f"Изображение сохранено в {file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())

import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from dct import DCT2D
from image_preparation import ImagePreparation
from quantize_bloks import QuantizeBlocks
from zigzag_transform import ZigzagTransform
from rle import RleProcessing

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Метка для изображения
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Кнопка для выбора изображения
        self.btn_open = QPushButton("Открыть изображение", self)
        self.btn_open.clicked.connect(self.open_image)
        layout.addWidget(self.btn_open)

        # Кнопка для запуска обработки
        self.btn_process = QPushButton("Обработать изображение", self)
        self.btn_process.clicked.connect(self.process_image)
        self.btn_process.setEnabled(False)
        layout.addWidget(self.btn_process)

        # Кнопка для сохранения результата
        self.btn_save = QPushButton("Сохранить изображение", self)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = None
        self.processed_image = None

    def open_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp *.jpeg)", options=options)
        if file_name:
            self.image_path = file_name
            self.show_image(self.image_path)
            self.btn_process.setEnabled(True)

    def show_image(self, path):
        # Загружаем изображение через OpenCV
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        # Масштабируем под размер окна
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def process_image(self):
        if not self.image_path:
            return
        
        # === Выполнение алгоритма ===
        pre_img = ImagePreparation(self.image_path)
        new_img = pre_img.pad_image_to_multiple()
        bloks = pre_img.split_into_bloks()

        res_dct = DCT2D()
        res_dct.apply_dct_to_blocks(bloks)

        quant_blocks = QuantizeBlocks()
        quant_blocks.quantize_dct_bloks(res_dct.dct_blocks)

        zig_ex = ZigzagTransform()
        zigzag_blocks = zig_ex.z_transform_blocks(quant_blocks.quantized_blocks)

        rle = RleProcessing()
        res_rle = rle.apply_rle_all_blocks(zigzag_blocks)
        restored_rle_blocks = rle.restore_rle_blocks()
        decoded_zigzag_blocks = rle.decode_rle_from_all_blocks()
        tr_blocks  = zig_ex.inverse_zigzag_transform_blocks()

        blocks_for_dct = quant_blocks.dequantize_blocks(tr_blocks, 8)
        blocks_pixels = res_dct.apply_idct_to_blocks(blocks_for_dct)
        reconstructed_image = pre_img.merge_blocks(blocks_pixels)
        reconstructed_bgr = cv2.cvtColor(reconstructed_image, cv2.COLOR_YCrCb2BGR)

        self.processed_image = reconstructed_bgr

        # Показать результат в интерфейсе
        self.display_processed_image(self.processed_image)

        # Активируем кнопку сохранения
        self.btn_save.setEnabled(True)

    def display_processed_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))

    def save_image(self):
        if self.processed_image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "",
                                                       "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
            if file_name:
                cv2.imwrite(file_name, self.processed_image)
                print(f"Изображение сохранено в {file_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())

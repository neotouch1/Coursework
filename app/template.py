import sys
import cv2
import os
import numpy as np
import time
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QPushButton, 
    QLabel, 
    QFileDialog, 
    QVBoxLayout, 
    QWidget,
    QDialog,
    QStatusBar,
    QSizePolicy
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from dct import DCT2D
from image_preparation import ImagePreparation
from quantize_bloks import QuantizeBlocks
from zigzag_transform import ZigzagTransform
from rle import RleProcessing
from UI.setting_dct import DCTSettingDialog
from UI.compression_lvl import CompressionLevelDialog

class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Processing App")
        self.setGeometry(100, 100, 1000, 800)

    # === Переменные для хранения данных ===
        self.image_path = None
        self.dct_choice = None
        self.compress_level = 50
        self.img_size_before = None
        self.img_size_after = None

        self.processed_image = None
        self.dct_blocks = None
        self.quantized_blocks = None
        self.zigzag_blocks = None
        self.rle_data = None


        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # === Метка для изображения ===
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        ### === Основные кнопки ===
        self.btn_open = QPushButton("Открыть изображение", self)
        self.btn_open.clicked.connect(self.open_image)
        layout.addWidget(self.btn_open)

        # === Задать выполнение DCT собственной реализации или библиотечной ===
        self.btn_dct = QPushButton("Выбрать реализацию DCT", self)
        self.btn_dct.clicked.connect(self.proc_dct)  # TODO function for processing (def dct2D(self, block):)
        layout.addWidget(self.btn_dct)


        # === Задать уровень сжатия ===
        self.btn_coeff = QPushButton("Задать уровень сжатия", self)
        self.btn_coeff.clicked.connect(self.set_compress_level) # TODO function for processing (scale_quantiztion_matrices)
        layout.addWidget(self.btn_coeff)



        self.btn_process = QPushButton("Обработать изображение", self)
        self.btn_process.clicked.connect(self.process_image)
        self.btn_process.setEnabled(False)
        layout.addWidget(self.btn_process)

        self.btn_save = QPushButton("Сохранить изображение", self)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        layout.addWidget(self.btn_save)

        ### ========================

        # === Кнопки для промежуточных шагов ===
        self.btn_show_dct = QPushButton("Показать карту DCT-коэффициентов", self)
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

        # # === Показать изменение размера изображения ===
        # self.btn_show_compressed = QPushButton("Показать степень сжатия", self)
        # self.btn_show_compressed.clicked.connect(self.none)  # TODO function for processing 
        # self.btn_show_compressed.setEnabled(False)
        # layout.addWidget(self.btn_show_compressed)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # self.image_size_label = QLabel("Размер изображения: -", self)
        # layout.addWidget(self.image_size_label)

        # self.processing_time_label = QLabel("Время обработки: -", self)
        # self.statusBar.addPermanentWidget(self.processing_time_label)
        self.image_size_label = QLabel("Размер: -", self)
        self.image_size_label.setStyleSheet("font-size: 20px; padding: 0 4px;")
        self.image_size_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.processing_time_label = QLabel("Время: -", self)
        self.processing_time_label.setStyleSheet("font-size: 20px; padding: 0 4px;")
        self.processing_time_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.statusBar.addWidget(self.image_size_label)  # Слева
        self.statusBar.addPermanentWidget(self.processing_time_label)
### ended UI init


### ==== Button image
    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")
        if file_name:
            self.image_path = file_name
            self.img_size_before = os.path.getsize(self.image_path)
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

### ====



### ==== Button "set DCT"
    def proc_dct(self):
        dialog = DCTSettingDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.dct_choice = dialog.selected_option()
            print(f"Выбрана реализация DCT: {self.dct_choice}")
### ====



### ==== Button "set compressed"

    def set_compress_level(self): # TODO function for processing (scale_quantiztion_matrices)
        dialog = CompressionLevelDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.compress_level = dialog.get_value()
            print(f"Уровень сжатия: {self.compress_level}%")
### ====


    def process_image(self):

        # create timer
        start_time = time.time()
        """
        Запуск обработки изображения:
        1. Подготовка изображения
        2. DCT преобразование
        3. Квантование
        4. Зигзагообразное преобразование
        5. RLE сжатие
        """

        pre_image = ImagePreparation(self.image_path)
        blocks = pre_image.split_into_bloks()

        res_dct = DCT2D()
        res_dct.apply_dct_to_blocks(blocks, self.dct_choice)

        quant_blocks = QuantizeBlocks()
        print(self.compress_level)
        quant_blocks.quantize_dct_bloks(res_dct.dct_blocks, self.compress_level)

        zig_ex = ZigzagTransform()
        zig_ex.z_transform_blocks(quant_blocks.quantized_blocks)

        rle = RleProcessing()
        self.rle_data = rle.apply_rle_all_blocks(zig_ex.zigzag_blocks)



        #Decode
        restored_rle_blocks = rle.restore_rle_blocks()


        decoded_zigzag_blocks = rle.decode_rle_from_all_blocks()
        tr_blocks  = zig_ex.inverse_zigzag_transform_blocks()


        blocks_for_dct = quant_blocks.dequantize_blocks(tr_blocks, 8) # Подготовка коэффициентов DCT
        blocks_pixels = res_dct.apply_idct_to_blocks(blocks_for_dct)

        # Собираем и сливаем блоки воедино
        reconstructed_image = pre_image.merge_blocks(blocks_pixels)
        reconstructed_bgr = cv2.cvtColor(reconstructed_image, cv2.COLOR_YCrCb2BGR)

        elapsed_time = time.time() - start_time
        self.processing_time_label.setText(f"Время обработки: {elapsed_time:.4f} сек")

        # 
        self.processed_image = reconstructed_bgr
        temp_file = "temp_compressed.jpg"
        cv2.imwrite(temp_file, self.processed_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
        self.img_size_after = os.path.getsize(temp_file)

        befor = round(self.img_size_before / 1024, 2)
        after = round(self.img_size_after / 1024, 2)
        # Обновляем метки в интерфейсе
        self.image_size_label.setText(f"Размер до: {befor} Кб, после: {after} Кб")
        # os.remove(temp_file)


    def save_image(self):
        if self.processed_image is not None:
            file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "JPEG Files (*.jpg)")
            if file_name:
                cv2.imwrite(file_name, self.processed_image, [cv2.IMWRITE_JPEG_QUALITY, 90])
                print(f"Изображение сохранено в {file_name}")


    def show_dct(self):
        """
        Отображение карты DCT коэффициентов для проверки результата.
        """
        pass

    def show_quantized_blocks(self):
        """
        Отображение квантованных блоков.
        """
        pass

    def show_zigzag(self):
        """
        Отображение результата зигзагообразного преобразования.
        """
        pass

    def show_rle(self):
        """
        Вывод результата RLE сжатия.
        """
        pass

    def save_image(self):
        """
        Сохранение обработанного изображения.
        """
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())

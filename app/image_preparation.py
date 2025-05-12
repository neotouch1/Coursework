import cv2
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt



class ImagePreparation:
    def __init__(self,
                 image_path, 
                 block_size=8
                 ):


        self.block_size = block_size
        print(f"Block_size: {self.block_size}")
        self.image_path = image_path
        self.image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)

        # self.image = cv2.GaussianBlur(img, (5, 5), 0)
        self.h = self.image.shape[0]
        self.w = self.image.shape[1]
        
        if self.image is None:
            raise FileNotFoundError("Image not loaded!")
        else:
            self.img_ycrcb = cv2.cvtColor(self.image, cv2.COLOR_BGR2YCrCb)
            print("File uploaded successfully!")
        



    def apply_subsampling(self):
        """
        Применяет субдискретизацию к компонентам Cb и Cr (например, 4:2:0).
        """
        if True:
            y, cr, cb = cv2.split(self.img_ycrcb)

            # Уменьшаем размерность Cb и Cr в 2 раза (субдискретизация 4:2:0)
            cr_resized = cv2.resize(cr, (self.w // 2, self.h // 2), interpolation=cv2.INTER_LINEAR)
            cb_resized = cv2.resize(cb, (self.w // 2, self.h // 2), interpolation=cv2.INTER_LINEAR)

            # Приводим y к размеру cr_resized и cb_resized, если необходимо
            if y.shape[:2] != cr_resized.shape[:2]:
                y = cv2.resize(y, (cr_resized.shape[1], cr_resized.shape[0]), interpolation=cv2.INTER_LINEAR)

            # Убедитесь, что все каналы имеют одинаковую глубину
            cr_resized = cr_resized.astype(np.uint8)
            cb_resized = cb_resized.astype(np.uint8)
            y = y.astype(np.uint8)

            # Объединяем каналы после приведения их к одинаковому размеру и типу
            self.img_ycrcb = cv2.merge([y, cr_resized, cb_resized])
            self.h = self.img_ycrcb.shape[0]
            self.w = self.img_ycrcb.shape[1]
            print(f"shape_sub_discret: {self.img_ycrcb.shape}")





    def pad_image_to_multiple(self):
        """
        Pad an image to make its dimensions a multiple of the block size.

        Args:
            img (numpy.ndarray): Input image of shape (height, width, channels).
            block_size (int, optional): Size of the block to pad to. Defaults to 8.

        Returns:
            numpy.ndarray: Padded image with dimensions aligned to the block size.
        """
        pad_h = (self.block_size - self.h % self.block_size) % self.block_size
        pad_w = (self.block_size - self.w % self.block_size) % self.block_size

        self.img_ycrcb = cv2.copyMakeBorder(self.img_ycrcb, 0, pad_h, 0, pad_w, cv2.BORDER_REPLICATE)
        self.h = self.img_ycrcb.shape[0]
        self.w = self.img_ycrcb.shape[1]

        print(f"resolutions: {self.img_ycrcb .shape}")

        return self.img_ycrcb
    

    def split_into_bloks(self):
        self.apply_subsampling()
        self.pad_image_to_multiple()
        """
        Split the padded image into blocks and store them in the field `self.blocks`.
        """

        blocks = self.img_ycrcb.reshape(self.h // self.block_size, self.block_size,
                                       self.w // self.block_size, self.block_size,
                                       self.img_ycrcb.shape[2])
        self.blocks = blocks.swapaxes(1, 2)
        return self.blocks




    def merge_blocks(self, blocks):
        """
        Собрать изображение из блоков.
        :param blocks: массив блоков (H, W, block_size, block_size, channels)
        :param original_shape: исходный размер изображения (h, w, channels)
        :return: восстановленное изображение
        """
        H, W, block_size, _, channels = blocks.shape
        h, w, _ = self.image.shape

        img = np.zeros((H * block_size, W * block_size, channels), dtype=np.uint8)

        for i in range(H):
            for j in range(W):
                img[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size, :] = blocks[i, j]

        return img[:h, :w]  # Обрезаем до исходного размера




# if __name__ == "__main__":
#     image_path = "/home/evgen/Coursework/dct_compress/-SZE57zExy0_600_338.jpg"

#     img = ImagePreparation(image_path)

#     new_img = img.pad_image_to_multiple()
#     bloks = img.split_into_bloks()
#     print(bloks.shape)

#     cv2.imshow("image", new_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
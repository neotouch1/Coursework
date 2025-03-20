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
        self.image_path = image_path
        self.image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        self.h = self.image.shape[0]
        self.w = self.image.shape[1]
        
        if self.image is None:
            raise FileNotFoundError("Image not loaded!")
        else:
            self.img_ycrcb = cv2.cvtColor(self.image, cv2.COLOR_BGR2YCrCb)
            print("File uploaded successfully!")
        
    

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

        return self.img_ycrcb
    

    def split_into_bloks(self):
        """
        Split the padded image into blocks and store them in the field `self.blocks`.
        """

        blocks = self.img_ycrcb.reshape(self.h // self.block_size, self.block_size,
                                       self.w // self.block_size, self.block_size,
                                       self.img_ycrcb.shape[2])
        self.blocks = blocks.swapaxes(1, 2)
        return self.blocks





# if __name__ == "__main__":
#     image_path = "/home/evgen/Coursework/dct_compress/-SZE57zExy0_600_338.jpg"

#     img = ImagePreparation(image_path)

#     new_img = img.pad_image_to_multiple()
#     bloks = img.split_into_bloks()
#     print(bloks.shape)

#     cv2.imshow("image", new_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
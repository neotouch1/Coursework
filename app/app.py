import cv2
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
from dct import DCT2D
from image_preparation import ImagePreparation


if __name__ == "__main__":
    image_path = "/home/evgen/Coursework/dct_compress/-SZE57zExy0_600_338.jpg"

    img = ImagePreparation(image_path)

    new_img = img.pad_image_to_multiple()
    bloks = img.split_into_bloks()
    print(bloks.shape)

    # cv2.imshow("image", new_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    res_dct = DCT2D()
    res_dct.apply_dct_to_blocks(bloks)
    print(res_dct.dct_blocks)
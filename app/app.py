import cv2
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
from dct import DCT2D
from image_preparation import ImagePreparation
from quantize_bloks import QuantizeBlocks
from zigzag_transform import ZigzagTransform
from rle import RleProcessing


if __name__ == "__main__":
    image_path = "/home/evgen/Coursework/dct_compress/-SZE57zExy0_600_338.jpg"

    pre_img = ImagePreparation(image_path)

    new_img = pre_img.pad_image_to_multiple()
    bloks = pre_img.split_into_bloks()
    print(bloks.shape)

    # cv2.imshow("image", new_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    res_dct = DCT2D()
    res_dct.apply_dct_to_blocks(bloks)
    #print(res_dct.dct_blocks)

    quant_blocks = QuantizeBlocks()
    quant_blocks.quantize_dct_bloks(res_dct.dct_blocks)
    #print(quant_blocks.quantized_blocks.shape)


    zig_ex = ZigzagTransform()
    # Преобразуем квантованные блоки
    zigzag_blocks = zig_ex.z_transform_blocks(quant_blocks.quantized_blocks)
    print("Зигзаг для первого блока канала Y:", zigzag_blocks[0, 0, :, 2])


    rle = RleProcessing()
    res_rle = rle.apply_rle_all_blocks(zigzag_blocks)
    #print(res_rle.shape)



    # Decode

    # Восстановление исходных блоков
    restored_rle_blocks = rle.restore_rle_blocks()
    #print(restored_rle_blocks)



    #decode rle
    decoded_zigzag_blocks = rle.decode_rle_from_all_blocks()
    tr_blocks  = zig_ex.inverse_zigzag_transform_blocks()
    #print(zigzag_blocks)

    
    # Проверим восстановление первого блока первого канала
    print("Декодированный первый блок (первый канал):")
    print(tr_blocks[0, 0, :, 2])
    print(tr_blocks.shape)

    blocks_for_dct = quant_blocks.dequantize_blocks(tr_blocks, 8) # Подготовка коэффициентов DCT

    # Обратное преобразование коэффициентов в пиксели
    blocks_pixels = res_dct.apply_idct_to_blocks(blocks_for_dct)
    print(blocks_for_dct.shape)

    # Собираем и сливаем блоки воедино
    reconstructed_image = pre_img.merge_blocks(blocks_pixels)
    
    reconstructed_bgr = cv2.cvtColor(reconstructed_image, cv2.COLOR_YCrCb2BGR)

    # Показать изображение
    cv2.imshow("Reconstructed Image", reconstructed_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Сохранить изображение
    cv2.imwrite("reconstructed_image.png", reconstructed_bgr)
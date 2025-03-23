import cv2
import numpy as np

class QuantizeBlocks:

    def __init__(self, q_matrix=None, quality=0):

        self.quality = quality

        if q_matrix is not None:
            self.q_matrices = q_matrix
        else:
            self.q_matrices = [
                np.array([  # Matrix for Y
                    [16, 11, 10, 16, 24, 40, 51, 61],
                    [12, 12, 14, 19, 26, 58, 60, 55],
                    [14, 13, 16, 24, 40, 57, 69, 56],
                    [14, 17, 22, 29, 51, 87, 80, 62],
                    [18, 22, 37, 56, 68, 109, 103, 77],
                    [24, 35, 55, 64, 81, 104, 113, 92],
                    [49, 64, 78, 87, 103, 121, 120, 101],
                    [72, 92, 95, 98, 112, 100, 103, 99]
                ]),
                np.array([  # Matrix for Cb
                    [17, 18, 24, 47, 99, 99, 99, 99],
                    [18, 21, 26, 66, 99, 99, 99, 99],
                    [24, 26, 56, 99, 99, 99, 99, 99],
                    [47, 66, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99]
                ]),
                np.array([  # Matrix for Cr
                    [17, 18, 24, 47, 99, 99, 99, 99],
                    [18, 21, 26, 66, 99, 99, 99, 99],
                    [24, 26, 56, 99, 99, 99, 99, 99],
                    [47, 66, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99],
                    [99, 99, 99, 99, 99, 99, 99, 99]
                ])
            ]


    def scale_quantiztion_matrices(self, quality):
        """
        Scales the base quantization matrices according to the desired quality.
    
        Args:
            base_matrices (list of np.array): Base quantization matrices for Y, Cb, and Cr.
            quality (int): The target quality in percentage (higher means better quality).
    
        Returns:
            list of np.array: Scaled quantization matrices corresponding to the input quality.
        """

        self.q_scale_matrices = [
            np.clip((m * quality + 50) / 100, 1, 255).astype(np.int32)
            for m in self.q_matrices
        ]

        return self.q_scale_matrices


    def quantize_dct_bloks(self, bloks, quality=0):
        """
        Quantizes the DCT coefficients using the selected quality factor.
        
        Args:
            blocks (np.array): DCT blocks to quantize.
            quality (int): Quality factor (0 = default matrices).
        
        Returns:
            np.array: Quantized blocks.
        """
        if quality == 0:
            H, W, block_size, _, channels = bloks.shape
            self.quantized_blocks = np.zeros_like(bloks, dtype=np.int32)

            for c in range(channels):
                for i in range(H):
                    for j in range(W):
                        self.quantized_blocks[i, j, :, :, c] = np.round(bloks[i, j, :, :, c] / self.q_matrices[c])

            return self.quantized_blocks
        
        else:
            self.scale_quantiztion_matrices(quality)
            H, W, block_size, _, channels = bloks.shape
            self.quantized_blocks = np.zeros_like(bloks, dtype=np.int32)


            for c in range(channels):
                for i in range(H):
                    for j in range(W):
                        self.quantized_blocks[i, j, :, :, c] = np.round(bloks[i, j, :, :, c] / self.q_scale_matrices[c])

            return self.quantized_blocks
        



        # Decoded
    def dequantize_blocks(self, quantized_blocks, block_size):
        """
        Восстановить коэффициенты DCT из квантованных значений.
        :param quantized_blocks: массив квантованных коэффициентов (H, W, block_size, block_size, channels)
        :param quality: параметр показывающий нужно спользовать встроенные матрицы квантования или кастомные
        :return: массив деквантованных коэффициентов DCT
        """
        #TODO  сделать по условию quality

        print(quantized_blocks.shape)
        H, W, block_size, _, channels = quantized_blocks.shape
        dct_blocks = np.zeros_like(quantized_blocks, dtype=np.float32)

        for c in range(channels):
            for i in range(H):
                for j in range(W):
                    dct_blocks[i, j, :, :, c] = quantized_blocks[i, j, :, :, c] * self.q_matrices[c]

        return dct_blocks
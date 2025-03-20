import cv2
import numpy as np

class QuantizeBloks:

    def __init__(self, q_matrix=None):

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

        if quality == 0:
            H, W, block_size, _, channels = bloks.shape
            quantized_blocks = np.zeros_like(bloks, dtype=np.int32)

            for c in range(channels):
                for i in range(H):
                    for j in range(W):
                        quantized_blocks[i, j, :, :, c] = np.round(bloks[i, j, :, :, c] / quant_matrices[c])

            return quantized_blocks
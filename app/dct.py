import cv2
import numpy as np
import os
import sys
import time
import matplotlib.pyplot as plt
from scipy.fftpack import dct


class DCT2D:
    def dct2Down(self, block):
        """
        Perform a 2D Discrete Cosine Transform (DCT) on a given square block.

        Args:
            block (numpy.ndarray): Input 2D array (block) of shape (N, N) representing the image block to transform.

        Returns:
            numpy.ndarray: Transformed 2D block with DCT applied, same shape as the input (N, N).

        """
        N = block.shape[0]
        dct_res = np.zeros((N, N), dtype=np.float32)
        alpha = lambda k : np.sqrt(1/N) if k == 0 else np.sqrt(2/N)

        for u in range(N):
            for v in range(N):
                sum_value = 0.0
                for x in range(N):
                    for y in range(N):
                        sum_value += block[x, y] * \
                                     np.cos((2 * x + 1) * u * np.pi / (2 * N)) * \
                                     np.cos((2 * y + 1) * v * np.pi / (2 * N))
                dct_res[u, v] = alpha(u) * alpha(v) * sum_value

        return dct_res
    


    def dct2D(self, block):
        """
        Perform a 2D Discrete Cosine Transform (DCT) using the scipy library.

        Args:
            block (numpy.ndarray): Input 2D array (block) of shape (N, N) representing the image block to transform.

        Returns:
            numpy.ndarray: Transformed 2D block with DCT applied, same shape as the input (N, N).
        """
        # Apply DCT on rows
        dct_rows = dct(block, axis=0, norm='ortho')
    
        # Apply DCT on columns
        dct_2d = dct(dct_rows, axis=1, norm='ortho')

        return dct_2d
    

    def apply_dct_to_blocks(self, blocks, use_own=False):
        """
        Apply 2D Discrete Cosine Transform (DCT) to all blocks, either using a custom implementation (own) or scipy.

        Args:
            blocks (numpy.ndarray): 4D array containing image blocks (num_blocks_x, block_size_x, num_blocks_y, block_size_y, channels).
            use_own (bool, optional): Whether to use the custom DCT implementation. Defaults to True.

        Returns: numpy.ndarray: 4D array with DCT applied to each block.
        """
        H, W, block_size, _, channels = blocks.shape
        self.dct_blocks = np.zeros_like(blocks, dtype=np.float32)

        # Применяем DCT к каждому блоку для каждого канала
        for i in range(H):
            for j in range(W):
                for c in range(channels):
                    block = blocks[i, j, :, :, c]  # Извлекаем блок для текущего канала
                    # dct_blocks[i, j, :, :, c] = dct2D(block)
                    block = np.float32(block)

                    if use_own:
                        self.dct_blocks[i, j, :, :, c] = self.dct2Down(block)
                    else:
                        self.dct_blocks[i, j, :, :, c] = self.dct2D(block)

        return self.dct_blocks
import numpy as np

class ZigzagTransform:

    """
    Class for performing zigzag transformation on DCT coefficient blocks.
    """
        
    def __init__(self, block_size=8):
        self.block_size = block_size
        print(f"Block_size: {self.block_size}")



    def z_blok2d(self, block):
        """
        Converts a 2D DCT coefficient block into a zigzag order.

        Args:
            block (np.ndarray): A 2D array of size (block_size, block_size) 
                representing the DCT coefficients of a single block.

        Returns:
            list: A 1D array of DCT coefficients in zigzag order.
        """
        block_size = block.shape[0]
        result = []
        for i  in range(2 * block_size - 1):
            if i % 2 == 0:
                for x in range(max(0, i - block_size + 1), min(i + 1, block_size)):
                    result.append(block[x, i - x])
            else:
                for x in range(max(0, i - block_size + 1), min(i + 1, block_size)):
                    result.append(block[i - x, x])
        return result
    
    
    def z_transform_blocks(self, quant_bloks):
        """
        Applies zigzag transformation to all DCT coefficient blocks.

        Args:
            quant_blocks (np.ndarray): A 5D array of shape 
                (H, W, block_size, block_size, channels) where:
                    H — number of blocks vertically
                    W — number of blocks horizontally
                    block_size — size of each DCT block (e.g., 8 for JPEG)
                    channels — number of channels (e.g., 1 for grayscale, 3 for RGB)

        Returns:
            np.ndarray: A 4D array of shape (H, W, block_size * block_size, channels)
                containing DCT coefficients in zigzag order.
        """
        H, W, block_size, _, channels = quant_bloks.shape
        self.zigzag_blocks = np.zeros((H, W, block_size * block_size, channels), dtype=np.int32)

        for c in range(channels):
            for i in range(H):
                for j in range(W):
                    self.zigzag_blocks[i, j, :, c] = self.z_blok2d(quant_bloks[i, j, :, :, c])

        return self.zigzag_blocks
    


    # Decoded
    def inverse_zigzag_scan(self, zigzag_array, block_size):
        """
        Преобразовать 1D-массив из зигзагообразного порядка обратно в 2D-блок.
        :param zigzag_array: 1D массив значений
        :param block_size: размер блока (block_size x block_size)
        :return: 2D массив
        """
        block = np.zeros((block_size, block_size), dtype=np.int32)
        index = 0
        for i in range(2 * block_size - 1):
            if i % 2 == 0:
                for x in range(max(0, i - block_size + 1), min(i + 1, block_size)):
                    block[x, i - x] = zigzag_array[index]
                    index += 1
            else:
                for x in range(max(0, i - block_size + 1), min(i + 1, block_size)):
                    block[i - x, x] = zigzag_array[index]
                    index += 1
        return block
    
    def inverse_zigzag_transform_blocks(self):
        """
        Преобразовать все блоки из зигзагообразного порядка обратно в 2D.
        :param zigzag_blocks: массив зигзагообразных преобразований (H, W, block_size*block_size, channels)
        :param block_size: размер блока (block_size x block_size)
        :return: массив блоков (H, W, block_size, block_size, channels)
        """
        H, W, _, channels = self.zigzag_blocks.shape

        blocks = np.zeros((H, W, self.block_size, self.block_size, channels), dtype=np.int32) #TODO сделать что-то с переменным размером блока

        for c in range(channels):
            for i in range(H):
                for j in range(W):
                    blocks[i, j, :, :, c] = self.inverse_zigzag_scan(self.zigzag_blocks[i, j, :, c], self.block_size)
        print(blocks.shape)
        return blocks
import numpy as np
import pickle

class RleProcessing:

    def __init__(self):
        pass

    def rle_encode(self, array):
        encoded = []
        prev_value = array[0]
        count = 1
        for val in array[1:]:
            if val == prev_value:
                count +=1
            else:
                encoded.append((prev_value, count))
                prev_value = val
                count = 1
        encoded.append((prev_value, count))
        return encoded
    
    def apply_rle_all_blocks(self, bloks):
        H, W, _, channels = bloks.shape
        self.rle_encoded_blocks = np.empty((H, W, channels), dtype=object)

        for c in range(channels):
            for i in range(H):
                for j in range(W):
                    self.rle_encoded_blocks[i, j, c] = self.rle_encode(bloks[i, j, :, c])

        return self.rle_encoded_blocks
    


    
    def optimize_rle_blocks(self):
        # Преобразуем массив в плоский список
        flat_list = self.rle_encoded_blocks.flatten()

        # Найдем уникальные элементы
        unique_blocks, inverse_indices = np.unique(flat_list, return_inverse=True)

        # Восстановим оригинальную форму с индексами уникальных элементов
        indices = inverse_indices.reshape(self.rle_encoded_blocks.shape)

        return unique_blocks, indices
    
    def restore_rle_blocks(self):
        """
        Восстановить исходные RLE-кодированные блоки из уникальных элементов и индексов.
        :param unique_blocks: уникальные элементы
        :param indices: индексы
        :return: восстановленные RLE-блоки
        """

        unique_blocks, indices = self.optimize_rle_blocks()
        # Восстановим плоский список с индексами
        restored_flat_list = unique_blocks[indices.flatten()]

        # Восстановим исходную форму
        self.restored_rle_blocks = restored_flat_list.reshape(indices.shape)

        return self.restored_rle_blocks
    


    def rle_decode(self, rle_data):
        """
        Декодировать массив, закодированный с помощью RLE.
        :param rle_data: массив пар (значение, количество)
        :return: декодированный 1D массив
        """
        decoded = []
        for value, count in rle_data:
            decoded.extend([value] * count)
        return decoded
    
    def decode_rle_from_all_blocks(self):
        """
        Применить декодирование RLE ко всем блокам.
        :param rle_encoded_blocks: массив RLE-кодированных блоков (H, W, channels)
        :return: массив зигзагообразных блоков (H, W, block_size^2, channels)
        """
        H, W, channels = self.restored_rle_blocks.shape
        # Предполагаем, что блокы квадратные и имеют одинаковый размер
        # Восстанавливаем размерность на основе количества элементов в одном блоке
        block_size_sq = len(self.rle_decode(self.restored_rle_blocks[0, 0, 0]))
        zigzag_blocks = np.zeros((H, W, block_size_sq, channels), dtype=np.int32)

        for c in range(channels):
            for i in range(H):
                for j in range(W):
                    zigzag_blocks[i, j, :, c] = self.rle_decode(self.restored_rle_blocks[i, j, c])

        return zigzag_blocks
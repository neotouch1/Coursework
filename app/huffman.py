import heapq
from collections import defaultdict


class HuffmanCoding:
    def __init__(self):
        self.huffman_tree = {}
        self.codes = {}
        
    def build_tree(self, data):
        freq = defaultdict(int)
        
        # Проходим по всем блокам
        for block in data:
            for item in block:
                # Проверяем, если item — это кортеж из 3 значений, например (value1, value2, count)
                if len(item) == 3:
                    value1, value2, count = item
                    freq[(value1, value2)] += count
                elif len(item) == 2:
                    value, count = item
                    freq[value] += count
                else:
                    print(f"Unexpected item structure: {item}")
        
        heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        
        self.codes = {}
        for weight, pair in heap:
            for symbol, code in pair:
                self.codes[symbol] = code
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









# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os

# # Создаём папку для сохранения графиков
# output_dir = "plots"
# os.makedirs(output_dir, exist_ok=True)

# # Загрузим CSV
# df = pd.read_csv("your_file.csv")

# # Установка стиля графиков
# sns.set(style="whitegrid")

# # Назначим названия столбцов
# if df.shape[1] > 5:
#     df.columns = ["Дата и время", "Время обработки (сек)", "Размер до (Кб)", "Размер после (Кб)", "Степень сжатия", "Ширина", "Высота"]
# else:
#     df.columns = ["Дата и время", "Время обработки (сек)", "Размер до (Кб)", "Размер после (Кб)", "Степень сжатия"]
#     df["Ширина"] = pd.NA
#     df["Высота"] = pd.NA

# # Преобразуем дату
# df["Дата и время"] = pd.to_datetime(df["Дата и время"], errors='coerce')

# # --- График 1: Время обработки от степени сжатия ---
# plt.figure(figsize=(10, 5))
# sns.boxplot(x="Степень сжатия", y="Время обработки (сек)", data=df)
# plt.title("Время обработки в зависимости от степени сжатия")
# plt.ylabel("Время обработки (сек)")
# plt.xlabel("Степень сжатия")
# plt.tight_layout()
# plt.savefig(os.path.join(output_dir, "time_vs_compression.png"))
# plt.close()

# # --- График 2: Размер до/после по степени сжатия ---
# plt.figure(figsize=(10, 5))
# sns.barplot(x="Степень сжатия", y="Размер до (Кб)", data=df, color="skyblue", label="До")
# sns.barplot(x="Степень сжатия", y="Размер после (Кб)", data=df, color="salmon", label="После")
# plt.legend()
# plt.title("Сравнение размера до и после по степени сжатия")
# plt.ylabel("Размер (Кб)")
# plt.xlabel("Степень сжатия")
# plt.tight_layout()
# plt.savefig(os.path.join(output_dir, "size_vs_compression.png"))
# plt.close()

# # --- График 3: Время обработки по разрешениям ---
# df_res = df.dropna(subset=["Ширина", "Высота"])
# df_res["Разрешение"] = df_res["Ширина"].astype(str) + "×" + df_res["Высота"].astype(str)

# plt.figure(figsize=(12, 6))
# sns.boxplot(x="Разрешение", y="Время обработки (сек)", data=df_res)
# plt.title("Время обработки по разрешениям")
# plt.ylabel("Время обработки (сек)")
# plt.xlabel("Разрешение")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig(os.path.join(output_dir, "time_vs_resolution.png"))
# plt.close()

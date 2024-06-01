import numpy as np

#1D FFT
def fft1d(signal):
    N = len(signal)
    if N <= 1:
        return signal
    even = fft1d(signal[0::2])
    odd = fft1d(signal[1::2])
    T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + [even[k] - T[k] for k in range(N // 2)]

#1D IFFT
def ifft1d(signal):
    N = len(signal)
    if N <= 1:
        return signal
    even = ifft1d(signal[0::2])
    odd = ifft1d(signal[1::2])
    T = [np.exp(2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
    return [(even[k] + T[k]) / 2 for k in range(N // 2)] + [(even[k] - T[k]) / 2 for k in range(N // 2)]

#2D FFT
def fft2d(image):
    # Преобразование каждой строки
    fft_rows = np.array([fft1d(row) for row in image])
    
    # Преобразование каждого столбца
    fft2d_result = np.array([fft1d(col) for col in fft_rows.T]).T
    
    return fft2d_result

#2D IFFT
def ifft2d(image):
    # Преобразование каждой строки
    ifft_rows = np.array([ifft1d(row) for row in image])
    
    # Преобразование каждого столбца
    ifft2d_result = np.array([ifft1d(col) for col in ifft_rows.T]).T
    
    return ifft2d_result

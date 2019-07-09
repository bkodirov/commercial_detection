import numpy as np


def xn(xs, n):
    '''
    calculate the Fourier coefficient X_n of
    Discrete Fourier Transform (DFT)
    '''
    l = len(xs)
    ks = np.arange(0, l, 1)
    xn = np.sum(xs * np.exp((1j * 2 * np.pi * ks * n) / l)) / l
    return xn


def get_xns(tone):
    '''
    Compute Fourier coefficients only up to the Nyquest Limit Xn, n=1,...,L/2
    and multiply the absolute value of the Fourier coefficients by 2,
    to account for the symetry of the Fourier coefficients above the Nyquest Limit.
    '''
    mag = []
    for n in range(len(tone) // 2):
        mag.append(np.abs(xn(tone, n)) * 2)
    return mag


def convert_fourie_coefficent_to_hz(fourie_c, sampling_rate, n_points):
    freq_hz = fourie_c * sampling_rate / n_points
    freq_hz = [int(i) for i in freq_hz]
    return freq_hz


def create_spectrogram(pcm, n_fft, noverlap=None):
    '''
    :param pcm:  original time series
    :param n_fft: The number of data points used in each block for the DFT.
    Fs:the number of points sampled per second, so called sample_rate
    :param noverlap: The number of points of overlap between blocks. The default value is 128.
    :return:
    '''
    if noverlap == None:
        noverlap = n_fft / 2
    noverlap = int(noverlap)
    starts = np.arange(0, len(pcm), n_fft - noverlap, dtype=int)
    # remove any window with less than NFFT sample size
    starts = starts[starts + n_fft < len(pcm)]
    xns = []
    for start in starts:
        # short term discrete fourier transform
        pcm_window = get_xns(pcm[start:start + n_fft])
        xns.append(pcm_window)
    specX = np.array(xns).T
    # rescale the absolute value of the spectrogram as rescaling is standard
    spec = 10 * np.log10(specX)
    assert spec.shape[1] == len(starts)
    return starts, spec

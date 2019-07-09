from src.analyze.ftt import get_xns, convert_fourie_coefficent_to_hz, create_spectrogram
from src.analyze.tone_generator import tone, sample_rate
import numpy as np
import pylab as plt


def show_tone_time_domain():
    total_ts_sec = len(tone) / sample_rate
    print("The total time series length = {} sec (N points = {}) ".format(total_ts_sec, len(tone)))
    plt.figure(figsize=(20, 3))
    plt.plot(tone)
    plt.xticks(np.arange(0, len(tone), sample_rate),
               np.arange(0, len(tone) / sample_rate, 1))
    plt.ylabel("Amplitude")
    plt.xlabel("Time (second)")
    plt.title("The total length of time series = {} sec, sample_rate = {}".format(len(tone) / sample_rate, sample_rate))
    plt.show()


def show_tone_frequency_domain():
    magnitudes = get_xns(tone)
    # the number of points to label along xaxis
    Nxlim = 5
    ks = np.linspace(0, len(magnitudes), Nxlim)
    ksHz = convert_fourie_coefficent_to_hz(ks, sample_rate, len(tone))
    plt.figure(figsize=(20, 3))
    plt.plot(magnitudes)
    plt.xticks(ks, ksHz)
    plt.xlabel("Frequency (k)")
    plt.title("Two-sided frequency plot")
    plt.ylabel("|Fourier Coefficient|")
    plt.show()
    print("show_tone_frequency_domain")


def plot_spectrogram(mappable=None):
    L = 256
    noverlap = 84
    starts, spec = create_spectrogram(tone, L, noverlap=noverlap)

    plt.figure(figsize=(20, 8))
    plt_spec = plt.imshow(spec, origin='lower')

    ## create ylim
    Nyticks = 10
    ks = np.linspace(0, spec.shape[0], Nyticks)
    ksHz = convert_fourie_coefficent_to_hz(ks, sample_rate, len(tone))
    plt.yticks(ks, ksHz)
    plt.ylabel("Frequency (Hz)")

    ## create xlim
    Nxticks = 10
    ts_spec = np.linspace(0, spec.shape[1], Nxticks)
    total_ts_sec = len(tone) / sample_rate
    ts_spec_sec = ["{:4.2f}".format(i) for i in np.linspace(0, total_ts_sec * starts[-1] / len(tone), Nxticks)]
    plt.xticks(ts_spec, ts_spec_sec)
    plt.xlabel("Time (sec)")

    plt.title("Spectrogram L={} Spectrogram.shape={}".format(L, spec.shape))
    plt.colorbar(mappable, use_gridspec=True)
    plt.show()
    return plt_spec


if __name__ == '__main__':
    # show_tone_time_domain()
    show_tone_frequency_domain()
    plot_spectrogram()

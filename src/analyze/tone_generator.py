import numpy as np


def generate_tone(hz, sample_rate, length_sec):
    # 1 sec length time series with sampling rate
    ts1sec = list(np.linspace(0, np.pi * 2 * hz, sample_rate))
    # 1 sec length time series with sampling rate
    ts = ts1sec * length_sec
    return list(np.sin(ts))


sample_rate = 4000
length_ts_sec = 3

# --------------------------------- ##
# 3 seconds of "digit 1" sound
# Pressing digit 2 buttom generates
# the sine waves at frequency
# 697Hz and 1209Hz.
# --------------------------------- ##
tone1 = np.array(generate_tone(697, sample_rate, length_ts_sec))  # Return type is numpy.ndarray
tone1 += np.array(generate_tone(1209, sample_rate, length_ts_sec))
tone1 = list(tone1)

# -------------------- ##
# 2 seconds of silence
# -------------------- ##
tone_silence = [0] * sample_rate * 2
tone2 = np.array(generate_tone(697, sample_rate, length_ts_sec))  # Return type is numpy.ndarray
tone2 += np.array(generate_tone(1336, sample_rate, length_ts_sec))
tone2 = list(tone2)

tone = tone1 + tone_silence + tone2



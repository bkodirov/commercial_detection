import wave
from pylab import *

from src.SlidingWindow import SlidingWindow


def print_audio_samples(wave_read: wave.Wave_read, pos_sec=0, steps=1, length_ms=2_000):
    rate = wave_read.getframerate()
    start_frame = rate * pos_sec
    wave_read.readframes(start_frame)
    end_frame = start_frame + (rate * length_ms // 1000)
    print("Reading from = %s to = %s, with step = %s" % (start_frame, end_frame, steps))
    string_buffer = []
    for i in range(start_frame, end_frame, steps):
        wave_read.setpos(i)
        peak = wave_read.readframes(1)
        string_buffer.append(str(peak[0]))
    print(','.join(string_buffer))


def print_audio_samples_all(wave_read: wave.Wave_read):
    n = wave_read.getnframes()
    buffer = []
    count = 0
    for i in range(n):
        sample = wave_read.readframes(1)
        int_version = int.from_bytes(sample, byteorder='little')
        if int_version == 0: count += 1
        if i % 100 == 0:
            # if int_version > (1 << 15): int_version = (1 << 15) - int_version
            buffer.append(int_version)
    print(buffer)
    print(count)


def calculate_relative_pos_ms(frame_index, frame_rate):
    return 1000 * frame_index // frame_rate


def find_silence(wav, percent=0):
    """
    This function assumes incoming PCM is 16 bit and mono
    """
    n = wav.getnframes()
    result = []
    start = None
    for i in range(n):
        sample = wav.readframes(1)
        int_version = int.from_bytes(sample, byteorder='little')
        if int_version > (1 << 15): int_version = (1 << 15) - int_version
        if abs(int_version) <= (1 << 15) * percent // 100:
            if start: continue

            print(int_version, 'is less then bar. Frame = ', i)
            start = i
        else:
            # Start point was found already
            if not start: continue

            result.append((start, i))
            start = None

    if start:  result.append((start, n))
    return result


def show_wave_n_spec(path):
    pcm = wave.open(path, 'r')
    print(pcm.getparams())
    sound_info = pcm.readframes(-1)
    sound_info = fromstring(sound_info, 'Int16')
    rate = pcm.getframerate()
    render(sound_info, rate)


def render(arr, rate):
    subplot(211)
    plot(arr)
    title('Wave from and spectrogram')

    subplot(212)
    spectrogram = specgram(arr, Fs=rate, scale_by_freq=True, sides='default')
    show()


def smooth_out(path):
    wav = wave.open(path, 'r')
    print(wav.getparams())
    n, rate = wav.getnframes(), wav.getframerate()
    window = SlidingWindow(1024)
    smooth_arr = []
    for _ in range(n // 2):
        ampl = int.from_bytes(wav.readframes(2), byteorder='big')
        window.add(ampl)
        smooth_arr.append(window.mean())
    render(smooth_arr, rate)
    wav.close()


if __name__ == "__main__":
    """
    Ads
    1. 08:19 - 12:24
    2. 18:36 - 21:54
    3. 30:54 - 34:20
    4. 43:25 - 46:04
    5. 53:28 - 57:15
    6. 1:00:00 - 
    """
    show_wave_n_spec("/Users/beka/proj/commercial_detection/examples/long/output/test.wav")
    # smooth_out("/Users/beka/proj/commercial_detection/examples/long/output/test.wav")

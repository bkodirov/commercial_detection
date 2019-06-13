import wave


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
    wav = wave.open("/Users/bekakodirov/projects/pyplayer/examples/long/output/concat.wav", 'rb')
    print(wav.getparams())
    print_audio_samples(wav, 495, 1, 2_000)
    wav.close()

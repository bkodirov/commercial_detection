import glob
from os import path
import wave

from m3u8 import M3U8

from src.utils import eprint

CONCAT_WAV = "concat.wav"


def create_combined_wav(folder_path: str, wav_file_path: str) -> wave.Wave_write:
    sample: wave.Wave_read = wave.open(wav_file_path, 'rb')
    concat_wav: wave.Wave_write = wave.open(path.join(folder_path, CONCAT_WAV), 'wb')
    concat_wav.setparams(sample.getparams())
    concat_wav.setnchannels(1)
    sample.close()
    return concat_wav


def concat_audio(folder_path, variant_playlist: M3U8):
    wav_files = glob.glob(path.join(folder_path, "*.wav"))
    if not wav_files:
        eprint("Folder doesn't contain any wav files")
        return
    file_name_dict = dict()
    for wav_file in wav_files:
        file_name = path.split(wav_file)[1].split('.')[0]
        file_name_dict[file_name] = wav_file

    output_wav = create_combined_wav(folder_path, wav_files[0])
    for segment in variant_playlist.segments:
        file_name = path.split(segment.uri)[1].split('.')[0]
        file_path = file_name_dict[file_name]
        chunk_reader: wave.Wave_read = wave.open(file_path, 'rb')
        output_wav.writeframes(chunk_reader.readframes(chunk_reader.getnframes()))
        chunk_reader.close()
    output_wav.close()

    # audio_segment = AudioSegment.from_wav(path.join(folder_path, CONCAT_WAV))
    # play(audio_segment)

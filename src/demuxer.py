import os
from subprocess import Popen, PIPE, call


def transportation_segment_demux(file_path: str):
    file_dir: str = os.path.split(file_path)[0]
    file_name: str = os.path.split(file_path)[1].split('.')[0]
    print("Demuxing", file_path, "started")
    file_path_template = os.path.join(file_dir, file_name)

    audio_extractor_cmd_str = "ffmpeg -hide_banner -y -i %s -acodec copy -vn %s.audio" % (file_path, file_path_template)
    video_extractor_cmd_str = "ffmpeg -hide_banner -y -i %s -vcodec copy -an -f rawvideo %s.video'" % (file_path, file_path_template)

    print(audio_extractor_cmd_str)
    print(video_extractor_cmd_str)

    # call(args_arr, shell=True)
    proc = Popen(audio_extractor_cmd_str.split(), stdout=PIPE, stderr=PIPE)
    o, e = proc.communicate()
    print(o.decode('utf-8'))
    print(e.decode('utf-8'))

    proc = Popen(video_extractor_cmd_str.split(), stdout=PIPE, stderr=PIPE)
    o, e = proc.communicate()
    print(o.decode('utf-8'))
    print(e.decode('utf-8'))

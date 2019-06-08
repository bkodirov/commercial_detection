import os
from subprocess import Popen, PIPE, call


def transportation_segment_demux(file_path: str):
    file_name: str = os.path.split(file_path)[1].split('.')[0]
    cmd_str = "ffmpeg -y -i %s -vcodec copy -an h264_%s.h264 -acodec copy -vn waw_%s.wav" % (file_path, file_name, file_name)
    print(cmd_str)
    args_arr = cmd_str.split()
    # call(args_arr, shell=True)
    proc = Popen(args_arr, stdout=PIPE, stderr=PIPE)
    o, e = proc.communicate()
    print(o)
    print(e)



if __name__ == "__main__":
    transportation_segment_demux('/Users/bekakodirov/projects/pyplayer/examples/akamai2/video/1080_4800000/hls/segment_0.ts')
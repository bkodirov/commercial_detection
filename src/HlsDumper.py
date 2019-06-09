import glob
from os import scandir
from urllib import request, parse
import m3u8
import os

from src.demuxer import transportation_segment_demux

BASE_EXAMPLES_PATH = os.path.abspath(os.path.join(os.getcwd(), '..', 'examples/'))


def main():
    with open('../examples/akamai/master.m3u8', 'r') as master_playlist:
        data = master_playlist.read()
    if not data:
        print("Couldn't parse playlist")
        return
    # print(data)
    m3u8_obj = m3u8.loads(data)
    for variant in m3u8_obj.playlists:
        # print(variant.uri)
        for media in variant.media:
            print(media)
        print('----')


def download_hls_files(folder_to_store, file_prefix, base_url, variant_hls):
    print("Started downloading playlist form ", base_url, "to", folder_to_store)
    for file in variant_hls.files:
        file_uri = parse.urljoin(base_url, file)
        print("fetching file", file_uri)
        # TODO Handle result properly
        file_destination = os.path.join(folder_to_store, file_prefix + os.path.split(file)[1])
        print("final_destination ", file_destination)
        request.urlretrieve(file_uri, file_destination)


def retrieve_m3u8_object(base_url, uri):
    # TODO handle uri. It might be relative or absolute path
    variant_url = parse.urljoin(base_url, uri)
    with request.urlopen(variant_url) as response:
        variant_data = response.read().decode('utf-8')
    # TODO Handle result properly
    print('---------------------')
    print(variant_data)
    print('---------------------')
    return m3u8.loads(variant_data)


def demux_downloaded_files(output_folder: str, file_prefix: str):
    for media_segment_path in glob.glob(os.path.join(output_folder, file_prefix + "*")):
        transportation_segment_demux(media_segment_path)


def generate_raw_stream(base_url, playlist_url, file_prefix, output_folder):
    media_playlist = retrieve_m3u8_object(base_url, playlist_url)
    download_hls_files(output_folder, file_prefix, base_url, media_playlist)
    demux_downloaded_files(output_folder, file_prefix)


def dump_stream(folder_name, url):
    stream_folder = os.path.join(BASE_EXAMPLES_PATH, folder_name)

    os.makedirs(stream_folder, exist_ok=True)
    with open(stream_folder + "/info.txt", 'w+') as info_file:
        info_file.write("Stream fetched from %s" % url)

    # Download the playlist download
    # TODO Handle result properly
    hls_playlist = retrieve_m3u8_object(url, '')
    # Download medias like (cc, audio etc)
    desired_audio_playlist = None
    for media_item in hls_playlist.media:
        if not media_item or media_item.autoselect:
            desired_audio_playlist = media_item

    high_bitrate_video_playlist = None
    if not hls_playlist.is_variant:
        for variant_playlist_obj in hls_playlist.playlists:
            if not high_bitrate_video_playlist or variant_playlist_obj.stream_info.bandwidth > high_bitrate_video_playlist.stream_info.bandwidth:
                high_bitrate_video_playlist = variant_playlist_obj
    else:
        high_bitrate_video_playlist = hls_playlist

    output_folder = os.path.join(stream_folder, "output")
    os.makedirs(output_folder, exist_ok=True)
    # Store audio on the output folder
    generate_raw_stream(url, desired_audio_playlist.uri, "audio_", output_folder)

    # Store audio on the output folder
    generate_raw_stream(url, high_bitrate_video_playlist.uri, "video_", output_folder)


if __name__ == "__main__":
    dump_stream("akamai2",
                'https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8')
    # dump_stream("fubo_hangoverIII", 'https://playlist-nonlive.fubo.tv/v4/finite.m3u8?hdnts=ip%3D74.90.241.179~st%3D1559885899~exp%3D1559972299~acl%3D%2F%2A~data%3D1559972299~hmac%3D61bd952f2c66028bc8ef837f5251bcb2584ad57f6bb9b2238640d359aca65a7c&watchToken=eyJhbGciOiJIUzI1NiIsInRva2VuVHlwZSI6IlVzYUZpbml0ZVdhdGNoVG9rZW4iLCJ0eXAiOiJKV1QifQ.eyJ3YXRjaFRva2VuIjp7ImNhbGxTaWduIjoiQU1DIiwiZGV2aWNlIjoiQUxMIiwiYmFuZHdpZHRoIjoiTUFTVEVSIiwiY291bnRyeSI6IlVTQSIsInVzZXJJZCI6ImJla2FAZnViby50diIsInJlcXVlc3RUeXBlIjoiZHZyIiwicmVnaW9uIjoid2VzdCIsInN0YXJ0IjoxNTU2MjIwNjAwLCJlbmQiOjE1NTYyMjc4NjB9LCJob21lWmlwIjoiMTAwMTkiLCJnZW9aaXAiOiIxMTIyNiJ9.vGddSHRqS13Oz2b4wpD0FRkPPQ2MHzbH5A4KTBJOOqU')

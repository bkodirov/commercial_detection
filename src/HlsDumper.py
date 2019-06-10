import glob
from urllib import parse

import m3u8
import os

import requests

from src.demuxer import transportation_segment_demux

__http_session__ = requests.Session()

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


def create_media_playlist_url(base_url, second_url):
    if bool(parse.urlparse(second_url).netloc):
        return second_url
    else:
        result = parse.urljoin(base_url, second_url)
        parse.urlparse(result)
        return result


def download_hls_files(folder_to_store, file_prefix, base_url, variant_hls):
    print("Started downloading playlist form ", base_url, "to", folder_to_store)
    for file in variant_hls.files:
        file_uri = create_media_playlist_url(base_url, file)
        print("fetching file", file_uri)
        # TODO Handle result properly
        file_destination = os.path.join(folder_to_store, file_prefix + os.path.split(file)[1])
        print("final_destination ", file_destination)
        with __http_session__.request('GET', file_uri) as response:
            with open(file_destination, 'wb') as local_copy:
                local_copy.write(response.content)


def retrieve_m3u8_object(base_url, uri):
    # TODO handle uri. It might be relative or absolute path
    try:
        variant_url = parse.urljoin(base_url, uri)
    except Exception:
        print("Can not join", base_url, uri)
    with __http_session__.request('GET', variant_url) as response:
        variant_data = response.text
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

    high_bitrate_video_playlist_uri = None
    if not hls_playlist.is_variant:
        hls_playlist.playlists.sort(key=lambda playlist: playlist.stream_info.bandwidth)
        high_bitrate_video_playlist_uri = hls_playlist.playlists[-1].uri
    else:
        high_bitrate_video_playlist_uri = url

    output_folder = os.path.join(stream_folder, "output")
    os.makedirs(output_folder, exist_ok=True)
    # Store audio on the output folder
    if desired_audio_playlist and desired_audio_playlist.uri:
        generate_raw_stream(url, desired_audio_playlist.uri, "audio_", output_folder)
    else:
        print("There is no independent audio playlist")
    # Store audio on the output folder
    generate_raw_stream(url, high_bitrate_video_playlist_uri, "video_", output_folder)


if __name__ == "__main__":
    # dump_stream("akamai2", 'https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8')
    dump_stream("long", 'https://dvr.fubo.tv/2019/04/24/N0347/010000-020100/media-8872332-sorted.m3u8?hdnts=ip%3D74.90.241.179~st%3D1560135065~exp%3D1560221465~acl%3D%2F%2A~data%3D1560221465~hmac%3D0dcfd96488c74331281f4023117e4682864a1b6ddde952d5654ebbfbf0e1c118')

import glob
from urllib import parse

import m3u8
import os

import requests
from m3u8 import Segment

from src.demuxer import transportation_segment_demux
from src.stream_decryptor import is_encrypted, decrypt_aes128cbc
from src.audio_processor import concat_audio

__http_session__ = requests.Session()

BASE_EXAMPLES_PATH = os.path.abspath(os.path.join(os.getcwd(), '..', 'examples/'))


def create_media_playlist_url(base_url, second_url):
    if bool(parse.urlparse(second_url).netloc):
        return second_url
    else:
        result = parse.urljoin(base_url, second_url)
        parse.urlparse(result)
        return result


def download_hls_files(folder_to_store, file_prefix, base_url, variant_hls):
    print("Started downloading playlist form ", base_url, "to", folder_to_store)
    for segment_obj in variant_hls.segments:
        segment_obj: Segment = segment_obj
        file_uri = create_media_playlist_url(base_url, segment_obj.uri)
        print("fetching segment_obj", file_uri)
        # TODO Handle result properly
        file_destination = os.path.join(folder_to_store, file_prefix + os.path.split(segment_obj.uri)[1])
        print("final_destination ", file_destination)
        with __http_session__.request('GET', file_uri) as response:
            media_segment_content = response.content
            if is_encrypted(segment_obj):
                with __http_session__.request('GET', segment_obj.key.uri) as key_response:
                    media_segment_content = decrypt_aes128cbc(media_segment_content, key_response.content,
                                                              segment_obj.key.iv)

            with open(file_destination, 'wb') as local_copy:
                local_copy.write(media_segment_content)


def retrieve_m3u8_object(base_url, uri):
    # TODO handle uri. It might be relative or absolute path
    try:
        variant_url = parse.urljoin(base_url, uri)
        with __http_session__.request('GET', variant_url) as response:
            variant_data = response.text
        # TODO Handle result properly
        print('---------------------')
        print(variant_data)
        print('---------------------')
        return m3u8.loads(variant_data)
    except Exception:
        print("Can not join", base_url, uri)


def demux_downloaded_files(output_folder: str, file_prefix: str):
    for media_segment_path in glob.glob(os.path.join(output_folder, file_prefix + "*")):
        transportation_segment_demux(media_segment_path)


def generate_raw_stream(base_url, playlist_url, file_prefix, output_folder):
    media_playlist = retrieve_m3u8_object(base_url, playlist_url)
    # download_hls_files(output_folder, file_prefix, base_url, media_playlist)
    # demux_downloaded_files(output_folder, file_prefix)
    concat_audio(output_folder, media_playlist)


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

    # high_bitrate_video_playlist_uri = url
    # if not hls_playlist.is_variant:
    #     hls_playlist.playlists.sort(key=lambda playlist: playlist.stream_info.bandwidth)
    #     high_bitrate_video_playlist_uri = hls_playlist.playlists[-1].uri
    # else:
    high_bitrate_video_playlist_uri = url

    output_folder = os.path.join(stream_folder, "output")
    os.makedirs(output_folder, exist_ok=True)
    # Store audio on the output folder
    if desired_audio_playlist and desired_audio_playlist.uri:
        generate_raw_stream(url, desired_audio_playlist.uri, "audio_", output_folder)
    else:
        print("There is no independent audio playlist")
    # Store video on the output folder
    generate_raw_stream(url, high_bitrate_video_playlist_uri, '', output_folder)


if __name__ == "__main__":
    # dump_stream("akamai2", 'https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8')

    """
    Ads
    1. 08:19 - 12:24
    2. 18:36 - 21:54
    3. 30:54 - 34:20
    4. 43:25 - 46:04
    5. 53:28 - 57:15
    6. 1:00:00 - 
    """
    dump_stream("long",
                'https://dvr.fubo.tv/2019/04/24/N0347/010000-020100/media-8872332-sorted.m3u8??hdnts=ip%3D74.90.241.179~st%3D1560395357~exp%3D1560481757~acl%3D%2F%2A~data%3D1560481757~hmac%3D4940adca4ac3461bb941d27e0a1fb6e559fec396fb1c8b6fbcddbb871802832d')

'openssl aes-128-cbc -d -in segment.ts -out out.ts -K d390a2db34a2d48fe220a2af87c38066 -iv B562114D9F8267ABD6A99EABCC361BF5'

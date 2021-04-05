import csv

import ffmpeg
from pytube import Playlist
from pytube import YouTube
from slugify import slugify


def download_video(video_link, folder, max_resolution=None):
    if max_resolution == None:

        print("Video Started")

        video_file = YouTube(video_link).streams.order_by('resolution').desc().first().download()

        print("Video Done")

    else:

        print("Video Started")

        video_file = YouTube(video_link).streams.filter(res=max_resolution).order_by(
            'resolution').desc().first().download()

        print("Video Done")

    video_name = slugify(video_file.replace(".webm", "").split("/")[-1])

    print("Audio Started")

    audio_file = YouTube(video_link).streams.filter(only_audio=True).order_by('abr').desc().first().download(
        filename_prefix="audio_")

    print("Audio Done")

    source_audio = ffmpeg.input(audio_file)
    source_video = ffmpeg.input(video_file)

    print("Concatenation Started")

    ffmpeg.concat(source_video, source_audio, v=1, a=1).output(f"{folder}/{video_name}.mp4").run()

    print("Concatenation Done")

    return None


def download_channel(channel_link, folder, maxres=None):
    pure_link = channel_link.replace("/featured", "/videos")

    list_videos = Playlist(pure_link).video_urls

    video_count = 0

    total_video = len(list_videos)

    print(f'{total_video} Videos Found')

    list_videos_downloaded = []

    with open('youtube_export_history.csv', 'r', newline='') as csvfile:

        spam_writer = csv.reader(csvfile, quoting=csv.QUOTE_MINIMAL)

        for row in spam_writer:
            list_videos_downloaded.append(row[0])

    for video in list_videos:

        if video in list_videos_downloaded:

            video_count = video_count + 1

            print(f'Video {video_count}/{total_video} already downloaded')

        else:

            print(video)

            video_count = video_count + 1

            print(f'{video_count}/{total_video} Started')

            download_video(video_link=video, max_resolution=maxres, folder=folder)

            with open('youtube_export_history.csv', 'a', newline='') as csvfile:
                spam_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                spam_writer.writerow([video])

            print(f'{video_count}/{total_video} Done')


download_channel(channel_link="channel_link",
                 folder="full_folder_path",
                 maxres=None)

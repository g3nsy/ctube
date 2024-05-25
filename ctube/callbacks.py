import os
import sys
import shutil
import eyed3
from pydub import AudioSegment
from ctube.containers import DownloadData


def on_progress_callback(
        download_data: DownloadData,
        filesize: int, 
        bytes_received: int, 
) -> None:
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * 0.40)
    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = "#" * filled + "-" * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)

    distance_from_bar = columns - (max_width + 9)  # len bar + percentage len
    title = f":: {download_data.title} "

    if len(title) > distance_from_bar:
        title = f"{title[:distance_from_bar - 4]}... "
    else:
        title = f"{title}{' ' * (distance_from_bar - len(title))}"

    text = f"{title}[{progress_bar}] {percent}%\r"

    sys.stdout.write(text)
    sys.stdout.flush()


def on_complete_callback(download_data: DownloadData) -> None:
    output = f"{os.path.splitext(download_data.filepath)[0]}.mp3"
    mp4 = AudioSegment.from_file(download_data.filepath, "mp4")
    mp4.export(output, format="mp3")
    audio = eyed3.load(output)
    if audio and audio.tag:
        audio.tag.title = download_data.title
        audio.tag.artist = download_data.artist
        audio.tag.album = download_data.album
        audio.tag.release_year = download_data.release_year
        audio.tag.tracks_num = download_data.tracks_num
        audio.tag.images.set(3, download_data.image_data, "image/jpeg", u"cover")
        audio.tag.save()
    os.remove(download_data.filepath)
    print()

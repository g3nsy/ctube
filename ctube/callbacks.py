import os
import sys
import shutil
import eyed3
from pydub import AudioSegment
from ctube.containers import Song


def on_progress_callback(
        song: Song,
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
    title = f":: {song.title} "

    if len(title) > distance_from_bar:
        title = f"{title[:distance_from_bar - 4]}... "
    else:
        title = f"{title}{' ' * (distance_from_bar - len(title))}"

    text = f"{title}[{progress_bar}] {percent}%\r"

    sys.stdout.write(text)
    sys.stdout.flush()


def on_complete_callback(song: Song) -> None:
    output = f"{os.path.splitext(song.filepath)[0]}.mp3"
    mp4 = AudioSegment.from_file(song.filepath, "mp4")
    mp4.export(output, format="mp3")
    set_metadata(filepath=output, song=song)
    os.remove(song.filepath)


def set_metadata(filepath: str, song: Song) -> None:
    audio = eyed3.load(filepath)
    album = song.album
    if audio and audio.tag:
        tag = audio.tag
        # Song tag
        tag.title = song.title
        tag.artist = song.artist
        tag.track_num = song.track_num
        tag.images.set(3, song.image_data, "image/jpeg", u"cover")

        # Album tag
        # eyed3.tag supported album_type values:
        # lp, ep, compilation, live, various, demo, sigle
        album_type = album.album_type.lower()
        if album_type != "album":
            try:
                tag.album_type = album_type 
            except ValueError:
                pass  # TODO: log error
        tag.album = album.title
        tag.release_year = album.release_year
        tag.save()

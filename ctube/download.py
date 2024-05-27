import os
from pathvalidate import sanitize_filename
from enum import Enum
from urllib import request
from urllib.error import HTTPError
from typing import Callable, List
from ctube.containers import Album, Song
from pytubefix import Playlist, Stream, YouTube
from pytubefix.exceptions import (
        MembersOnly, 
        RecordingUnavailable, 
        VideoPrivate, 
        VideoUnavailable
)


class BaseURL(str, Enum):
    PLAYLIST = "https://music.youtube.com/playlist?list="


class Downloader:
    def __init__(
            self,
            output_path: str,
            on_complete_callback: Callable[[Song], None],
            on_progress_callback: Callable[[Song, int, int], None],
            skip_existing: bool = False
    ):
        self.output_path = output_path
        self.on_complete_callback = on_complete_callback 
        self.on_progress_callback = on_progress_callback
        self.skip_existing = skip_existing

    @property
    def output_path(self) -> str:
        return self._output_path

    @output_path.setter
    def output_path(self, output_path: str) -> None:
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
        if not os.path.isdir(output_path):
            raise NotADirectoryError
        if not os.access(path=output_path, mode=os.W_OK):
            raise NotADirectoryError
        self._output_path = output_path

    def _on_complete_callback(self, data: Song, filepath: str) -> None:
        data.filepath = filepath
        self.on_complete_callback(data)

    def _on_progress_callback(self, data: Song, bytes_remaining: int, stream: Stream) -> None:
        filesize = stream.filesize
        bytes_received = filesize - bytes_remaining
        self.on_progress_callback(data, filesize, bytes_received)

    def download(self, album: Album, artist: str) -> List[YouTube]:
        playlist = Playlist(url=f"{BaseURL.PLAYLIST.value}{album.playlist_id}")
        failed_downloads: List[YouTube] = []

        response = request.urlopen(album.thumbnail_url)
        image_data = response.read()

        final_destination = os.path.join(
            os.path.join(
                self.output_path, sanitize_filename(artist)
            ), 
            sanitize_filename(album.title)
        )

        os.makedirs(final_destination, exist_ok=True)

        for i, url in enumerate(playlist):
            youtube = YouTube(url=url)

            try:
                stream = youtube.streams
            except (
                    MembersOnly, 
                    RecordingUnavailable, 
                    VideoPrivate, 
                    VideoUnavailable,
                    KeyError  # This is a bug in pytubefix I think.
            ):
                failed_downloads.append(youtube)
                continue

            audio_stream = stream.get_audio_only(subtype="mp4")

            if not audio_stream:
                failed_downloads.append(youtube)
                continue

            song = Song(
                title=youtube.title,
                artist=artist,
                track_num=i + 1,
                image_data=image_data,
                filepath="",
                album=album
            )

            youtube.register_on_progress_callback(
                lambda stream, _, bytes_remaining: self._on_progress_callback(
                    song, bytes_remaining, stream
                )
            )
            youtube.register_on_complete_callback(
                lambda _, filepath: self._on_complete_callback(
                    song, 
                    filepath  # type: ignore
                    # pytubefix says that 'filepath' can be None, 
                    # but this is not possible.
                )
            )

            try:
                audio_stream.download(
                    output_path=final_destination,
                    skip_existing=self.skip_existing
                )
            except HTTPError:
                failed_downloads.append(youtube)

        return failed_downloads

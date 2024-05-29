import os
from urllib.error import HTTPError, URLError
from pathvalidate import sanitize_filename
from http.client import IncompleteRead
from enum import Enum
from typing import Callable, Generator
from ctube.containers import Album, Song
from pytubefix import Playlist, Stream, YouTube
from pytubefix.exceptions import VideoUnavailable
from ctube.errors import NoMP4StreamAvailable, EmptyStreamQuery


class BaseURL(str, Enum):
    PLAYLIST = "https://music.youtube.com/playlist?list="


class Downloader:
    def __init__(
            self,
            output_path: str,
            on_complete_callback: Callable[[Song], None],
            on_progress_callback: Callable[[Song, int, int], None],
            skip_existing: bool = False,
            timeout: int = 5,
            max_retries: int = 2
    ):
        self.output_path = output_path
        self.on_complete_callback = on_complete_callback 
        self.on_progress_callback = on_progress_callback
        self.skip_existing = skip_existing
        self.timeout = timeout
        self.max_retries = max_retries

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

    def download_album(
            self, 
            album: Album, 
            artist: str, 
            image_data: bytes, 
    ) -> Generator:
        output_path = os.path.join(
            os.path.join(
                self.output_path, sanitize_filename(artist)
            ), 
            sanitize_filename(album.title)
        )
        os.makedirs(output_path, exist_ok=True)

        playlist = Playlist(url=f"{BaseURL.PLAYLIST.value}{album.playlist_id}")
        for i, url in enumerate(playlist):
            youtube = YouTube(url=url)

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
                    filepath  # type: ignore | another problem with pytubefix ?
                )
            )

            try:
                self._download_song(youtube, output_path=output_path)
            except (
                    VideoUnavailable,
                    IncompleteRead, 
                    TimeoutError,
                    EmptyStreamQuery,
                    NoMP4StreamAvailable,
                    HTTPError,
                    URLError,
                    KeyError # https://github.com/JuanBindez/pytubefix/issues/88
            ) as err:
                error = err
            else:
                error = None

            yield song, error

    def _download_song(self, youtube: YouTube, output_path: str) -> None:
        streams = youtube.streams
        if not len(streams):
            raise EmptyStreamQuery(f"The song '{youtube.title}' did not provide any data streams")
        else:
            stream = streams.get_audio_only(subtype="mp4")
            if stream is None:
                raise NoMP4StreamAvailable("Unexpected status: MP4 stream unavailable")

        stream.download(
            output_path=output_path,
            skip_existing=self.skip_existing,
            timeout=self.timeout,
            max_retries=self.max_retries
        )

import ctube
import sys
from requests.exceptions import RequestException
from typing import List, Optional, Tuple
from urllib import request
from urllib.error import URLError
from innertube.clients import InnerTube
from ctube.update import get_latest_version
from ctube.download import Downloader
from ctube.errors import InvalidIndexSyntax
from ctube.terminal import Prompt
from ctube.containers import Album
from ctube.colors import Color
from ctube.cmds import Command
from ctube.helpers import (
    filter_albums_by_indexes, 
    filter_albums_by_regex,
    handle_connection_errors,
    connected_to_internet
)
from ctube.parser import parse_user_input
from ctube.callbacks import (
    on_progress_callback, 
    on_complete_callback
)
from ctube.printers import (
    clear_screen,
    print_albums_list,
    print_albums_dict,
    print_header, 
    print_help, 
    write
)
from ctube.extractors import (
    extract_artist_id, 
    extract_albums
)


class App:
    def __init__(
            self, 
            output_path: str,
            skip_existing: bool = True,
            timeout: int = 5,
            max_retries: int = 3
    ):
        self.client = InnerTube("WEB_REMIX")
        self.prompt = Prompt()
        self.downloader = Downloader(
            output_path=output_path, 
            skip_existing=skip_existing,
            on_complete_callback=on_complete_callback,
            on_progress_callback=on_progress_callback,
            timeout=timeout,
            max_retries=max_retries
        )

        # last search
        self._albums: Optional[List[Album]] = None
        self._artist_name: Optional[str] = None

    def main_loop(self) -> None:
        clear_screen()
        print_header()
        try:
            latest_version = get_latest_version("ctube")
        except RequestException:
            pass
        else:
            if latest_version > ctube.__version__:
                print(f"=> New version available: {latest_version}")
                print(f"=> Close and run 'pip install -U ctube' to update.")
            else:
                print("=> ctube is up to date")
        while True:
            user_input = self.prompt.get_input().strip()

            if not user_input: 
                continue

            cmd_name, args = parse_user_input(user_input)

            try:
                cmd = Command.get_by_name(cmd_name)
            except KeyError:
                write(f"Invalid command: {cmd_name}", Color.RED)
            else:
                match cmd:
                    case Command.EXIT:
                        App._exit()
                    case Command.CLEAR:
                        clear_screen()
                    case Command.HELP:
                        print_help()
                    case Command.SEARCH:
                        self._search(args)
                    case Command.ID:
                        self._id(args)
                    case Command.DOWNLOAD:
                        self._download(args)
                    case Command.FILTER:
                        self._filter(args)

    @handle_connection_errors
    def _search(self, artist_name: str) -> None:
        if not artist_name:
            write("Missing argument: artist name", Color.RED)
        else:
            data = self.client.search(artist_name)
            try:
                artist_id = extract_artist_id(data)
            except (KeyError, TypeError, IndexError):
                write(f"Artist '{artist_name}' not found", Color.RED)
            else:
                self._id(artist_id)

    @handle_connection_errors
    def _id(self, artist_id: str) -> None:
        if not artist_id:
            write("Missing argument: artist id", Color.RED)
        else:
            data = self.client.browse(f"MPAD{artist_id}")
            try:
                artist_music_data = extract_albums(data)
            except (KeyError, TypeError, IndexError):
                write(f"Content not found", Color.RED)
            else:
                artist_music_data: Tuple[List[Album], str]
                self._albums, self._artist_name = artist_music_data
                self._albums.sort(key=lambda x: x.title)
                write(f"Collected music for {self._artist_name}", Color.GREEN)
                print_albums_list(self._albums)

    def _download(self, indexes: str):
        if not self._albums or not self._artist_name:
            write("You need to search for music first.", Color.RED)
            write("Use the search/id command", Color.RED)
        elif not indexes:
            write("Missing argument: indexes", Color.RED)
        elif not connected_to_internet():
            write("No internet connection", Color.RED)
        else:
            try:
                albums = filter_albums_by_indexes(self._albums, indexes)
            except InvalidIndexSyntax as error:
                write(str(error), Color.RED)
            else:
                print('\033[?25l', end="")
                if len(albums) == len(self._albums):
                    write(f"Selected items: ALL", Color.BLUE)
                else:
                    write(f"Selected items:", Color.BLUE)

                for album in albums:
                    write(f"\u2022 {album.title}", Color.BOLD)

                for album in albums:
                    write(f":: Downloading: {album.title}", Color.GREEN)

                    try:
                        response = request.urlopen(album.thumbnail_url)
                        image_data = response.read()
                    except URLError:
                        write(f"An error occurred while downloading {album.title} cover art", Color.RED)
                        write(f"Skipping {album.title}", Color.YELLOW)
                    else:
                        for song, error in self.downloader.download_album(
                                album=album, 
                                artist=self._artist_name,
                                image_data=image_data
                        ):
                            print()
                            if error:
                                write(f"An error occurred while downloading {song.title}", Color.RED)
                                write(f"Reason: {str(error)}", Color.RED)
                print('\033[?25h', end="")

    def _filter(self, pattern: str) -> None:
        if not self._albums or not self._artist_name:
            write("You need to search for music first.", Color.RED)
            write("Use the search/id command", Color.RED)
        elif not pattern:
            write("Missing argument: pattern", Color.RED)
        else:
            filtered_albums = filter_albums_by_regex(self._albums, pattern=pattern)
            if filtered_albums:
                print_albums_dict(filtered_albums)
            else:
                write(f"No match found", Color.RED)

    @staticmethod
    def _exit():
        sys.stdout.write('\033[?25h')
        sys.exit(0)

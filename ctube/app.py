import sys
from typing import List, Optional, Tuple
from urllib.error import URLError
from innertube.clients import InnerTube
from ctube.download import Downloader
from ctube.errors import InvalidIndexSyntax
from ctube.terminal import Prompt
from ctube.containers import MusicItem
from ctube.colors import Color
from ctube.cmds import Command
from ctube.helpers import (
    get_filtered_music_items, 
    handle_connection_errors,
    connected_to_internet
)
from ctube.parser import parse_user_input
from ctube.callbacks import (
    on_progress_callback, 
    on_complete_callback
)
from ctube.printers import (
    print_header, 
    print_help, 
    print_music_items,
    write,
    clear_screen
)
from ctube.extractors import (
    extract_artist_id, 
    extract_artist_music
)


class App:
    def __init__(
            self, 
            output_path: str,
            skip_existing: bool = True,
    ):
        self.client = InnerTube("WEB_REMIX")
        self.prompt = Prompt()
        self.downloader = Downloader(
            output_path=output_path, 
            skip_existing=skip_existing,
            on_complete_callback=on_complete_callback,
            on_progress_callback=on_progress_callback
        )

        # last search
        self._music_items: Optional[List[MusicItem]] = None
        self._artist_name: Optional[str] = None

    def main_loop(self) -> None:
        clear_screen()
        print_header()
        while True:
            user_input = self.prompt.get_input()
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
                artist_music_data = extract_artist_music(data)
            except (KeyError, TypeError, IndexError):
                write(f"Content not found", Color.RED)
            else:
                artist_music_data: Tuple[List[MusicItem], str]
                self._music_items, self._artist_name = artist_music_data
                write(f"Collected music for {self._artist_name}", Color.GREEN)
                print_music_items(self._music_items)

    def _download(self, indexes: str):
        if not self._music_items or not self._artist_name:
            write("You need to search for music first.", Color.RED)
            write("Use the search/id command", Color.RED)
        elif not indexes:
            write("Missing argument: indexes", Color.RED)
        elif not connected_to_internet():
            write("No internet connection", Color.RED)
        else:
            try:
                filtered_items = get_filtered_music_items(self._music_items, indexes)
            except InvalidIndexSyntax as error:
                write(str(error), Color.RED)
            else:
                print('\033[?25l', end="")
                if len(filtered_items) == len(self._music_items):
                    write(f"Selected items: ALL", Color.BLUE)
                else:
                    write(f"Selected items:", Color.BLUE)
                for item in filtered_items:
                    write(f"\u2022 {item.title}", Color.BOLD)

                for item in filtered_items:
                    write(f":: Downloading: {item.title}", Color.GREEN)
                    try:
                        self.downloader.download(item=item, artist=self._artist_name)
                    except (URLError, TimeoutError) as error:
                        write(f"A connection error occurred while downloading: {item.title}", Color.RED)
                        write(f"Reason: {str(error)}", Color.RED)
                        break
                print('\033[?25h', end="")

    @staticmethod
    def _exit():
        sys.stdout.write('\033[?25h')
        sys.exit(0)

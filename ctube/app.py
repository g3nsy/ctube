import sys
from typing import List, Optional, Tuple
from innertube.clients import InnerTube
from innertube.errors import RequestError
from ctube.download import Downloader
from ctube.terminal import Prompt
from ctube.containers import MusicItem
from ctube.colors import color, Color
from ctube.cmds import Commands
from ctube.errors import (
    ArtistNotFoundError,
    ContentNotFoundError,
    CommandNotFoundError
)
from ctube.callbacks import (
    on_progress_callback, 
    on_complete_callback
)
from ctube.helpers import (
    get_filtered_input,
    get_filtered_music_items,
)
from ctube.printers import (
    print_header, 
    print_info, 
    print_help, 
    print_music_items,
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
            cmd_name, args = get_filtered_input(user_input)
            if cmd_name not in [cmd.value.name for cmd in Commands]:
                print(color(f"Invalid command: {cmd_name}", Color.RED))
                continue
            else:
                cmd_obj = Commands.get_by_name(cmd_name)
                if not args and cmd_obj.value.required_args > 0:
                    print(color(
                        "Missing argument(s) "
                        f"{', '.join([arg.name for arg in cmd_obj.value.args])} for {cmd_name}", # type: ignore
                        Color.RED
                    ))
                    continue
            if cmd_name == Commands.EXIT.value.name:
                exit()
            elif cmd_name == Commands.CLEAR.value.name:
                clear_screen()
            elif cmd_name == Commands.HELP.value.name:
                print_help()
            elif cmd_name == Commands.INFO.value.name:
                print_info(args)
            elif cmd_name in (Commands.SEARCH.value.name, Commands.ID.value.name):
                self._do_search(cmd_name, args)
            elif cmd_name == Commands.DOWNLOAD.value.name:
                self._do_download(args)
            else:
                print(color("Invalid syntax", Color.RED))

    def _search(self, artist_name: str) -> Tuple[List[MusicItem], str]:
        data = self.client.search(artist_name)
        artist_id = extract_artist_id(data)
        if artist_id:
            return self._id(artist_id)
        else:
            raise ArtistNotFoundError

    def _id(self, artist_id: str) -> Tuple[List[MusicItem], str]:
        data = self.client.browse(artist_id)
        artist_music_data = extract_artist_music(data)
        artist_music_data: Optional[Tuple[List[MusicItem], str]]
        if artist_music_data:
            return artist_music_data
        else:
            raise ContentNotFoundError

    def _do_search(self, mode: str, arg: str) -> Optional[Tuple[List[MusicItem], str]]:
        if mode == "search":
            data = self.client.search(query=arg)
            artist_id = extract_artist_id(data)
            if not artist_id:
                print(color(f"Artist '{arg}' not found", Color.RED))
                return
        elif mode == "id":
            artist_id = arg
        else:
            raise CommandNotFoundError
        try:
            artist_music_data = self.client.browse(browse_id=f"MPAD{artist_id}")
        except RequestError:
            print(color(f"Invalid ID: {artist_id}", Color.RED))
        else:
            res = extract_artist_music(artist_music_data)
            if not res:
                print(color(f"Content not found", Color.RED))
            else:
                res: Tuple[List[MusicItem], str]
                self._music_items, self._artist_name = res
                print(color(f"Collected music for {self._artist_name}", Color.GREEN))
                print_music_items(self._music_items)

    def _do_download(self, user_input: str):
        if not self._music_items or not self._artist_name:
            print(color("You need to search for music first. Use the search command", Color.RED))
            return
        filtered_items = get_filtered_music_items(self._music_items, user_input)
        if filtered_items:
            print('\033[?25l', end="")
            if len(filtered_items) == len(self._music_items):
                print(color(f"Selected items: ALL", Color.BLUE))
            else:
                print(color(f"Selected items:", Color.BLUE))
            for item in filtered_items:
                print(color(f"\u2022 {item.title}", Color.BOLD))

            for item in filtered_items:
                print(color(f":: Downloading: {item.title}", Color.GREEN))
                self.downloader.download(item=item, artist=self._artist_name)
                print('\033[?25h', end="")
def exit():
    sys.stdout.write('\033[?25h')
    sys.exit(0)

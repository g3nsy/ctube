import os
import sys
import shutil
import pydub
import eyed3
from typing import List, Optional, Tuple
from innertube.clients import InnerTube
from innertube.errors import RequestError
from ctube.download import Downloader
from ctube.terminal import Prompt
from ctube.errors import InvalidSyntax
from ctube.containers import MusicItem
from ctube.colors import color, Color
from ctube.download import Data
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
from ctube.cmds import (
    Commands, 
    get_available_cmds_names, 
    get_cmd_by_name,
    get_cmd_with_args, 
    is_command
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

            if cmd_name not in get_available_cmds_names():
                print(color(f"Invalid command: {cmd_name}", Color.RED))
                continue
            else:
                cmd_obj = get_cmd_by_name(cmd_name)
                if not args and cmd_obj in get_cmd_with_args():
                    print(color(f"Missing argument {cmd_obj.value.expected_args} for {cmd_name}", Color.RED))
                    continue

            if is_command(user_input, Commands.EXIT):
                exit()
            elif is_command(user_input, Commands.CLEAR):
                clear_screen()
            elif is_command(user_input, Commands.HELP):
                print_help()
            elif is_command(cmd_name, Commands.INFO):
                print_info(args)
            elif is_command(cmd_name, Commands.SEARCH) or is_command(cmd_name, Commands.ID):
                self._do_search(cmd_name, args)
            elif is_command(cmd_name, Commands.DOWNLOAD):
                self._do_download(args)
            else:
                print(color("Invalid syntax", Color.RED))

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
            raise InvalidSyntax
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

def on_progress_callback(
        data: Data,
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
    title = f":: {data.title} "

    if len(title) > distance_from_bar:
        title = f"{title[:distance_from_bar - 4]}... "
    else:
        title = f"{title}{' ' * (distance_from_bar - len(title))}"

    text = f"{title}[{progress_bar}] {percent}%\r"

    sys.stdout.write(text)
    sys.stdout.flush()


def on_complete_callback(data: Data) -> None:
    output = f"{os.path.splitext(data.filepath)[0]}.mp3"

    mp4 = pydub.AudioSegment.from_file(data.filepath, "mp4")
    mp4.export(output, format="mp3")

    audio = eyed3.load(output)
    if audio and audio.tag:
        audio.tag.title = data.title
        audio.tag.artist = data.artist
        audio.tag.album = data.album
        audio.tag.release_year = data.release_year
        audio.tag.tracks_num = data.tracks_num
        audio.tag.images.set(3, data.image_data, "image/jpeg", u"cover")
        audio.tag.save()
        
    os.remove(data.filepath)
    print()


def exit():
    sys.stdout.write('\033[?25h')
    sys.exit(0)

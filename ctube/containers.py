from dataclasses import dataclass


@dataclass
class MusicItem:
    title: str
    item_type: str
    release_year: int
    thumbnail_url: str
    playlist_id: str


@dataclass
class DownloadData:
    title: str
    album: str
    artist: str
    release_year: int
    tracks_num: int
    image_data: bytes
    filepath: str

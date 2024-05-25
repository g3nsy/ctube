from dataclasses import dataclass


@dataclass(kw_only=True)
class MusicItem:
    title: str
    item_type: str
    release_year: int
    thumbnail_url: str
    playlist_id: str


@dataclass(kw_only=True)
class DownloadData:
    title: str
    album: str
    artist: str
    release_year: int
    tracks_num: int
    image_data: bytes
    filepath: str

from dataclasses import dataclass


@dataclass
class Album:
    title: str
    album_type: str
    release_year: int
    thumbnail_url: str
    playlist_id: str


@dataclass
class Song:
    title: str
    artist: str
    track_num: int
    image_data: bytes
    filepath: str
    album: Album

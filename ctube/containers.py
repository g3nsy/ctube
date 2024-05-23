class MusicItem:
    def __init__(
            self, 
            title: str, 
            item_type: str, 
            release_year: int, 
            thumbanail_url: str, 
            playlist_id: str
    ):
        self.title = title
        self.item_type = item_type
        self.release_year = release_year
        self.thumbanail_url = thumbanail_url
        self.playlist_id = playlist_id

from typing import Dict, List, Tuple
from ctube.containers import MusicItem


def extract_artist_id(data: Dict) -> str:
    return data["contents"]["tabbedSearchResultsRenderer"][
        "tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"][
        "contents"][1]["musicCardShelfRenderer"]["title"]["runs"][0][
        "navigationEndpoint"]["browseEndpoint"]["browseId"]


def extract_artist_music(data: Dict) -> Tuple[List[MusicItem], str]:
    music_items: List[MusicItem] = []
    for item in data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0][
        "tabRenderer"]["content"]["sectionListRenderer"]["contents"][
        0]["gridRenderer"]["items"]:

        item_data = item["musicTwoRowItemRenderer"]
        item_type = item_data["subtitle"]["runs"][0]["text"]
        title = item_data["title"]["runs"][0]["text"]
        release_year = int(item_data["subtitle"]["runs"][-1]["text"])
        thumbanail_url = item_data["thumbnailRenderer"][
            "musicThumbnailRenderer"]["thumbnail"][
            "thumbnails"][-1]["url"]
        playlist_id = item_data["menu"]["menuRenderer"]["items"][
            0]["menuNavigationItemRenderer"]["navigationEndpoint"][
            "watchPlaylistEndpoint"]["playlistId"]
        music_items.append(
            MusicItem(
                title=title, 
                item_type=item_type,
                release_year=release_year,
                thumbanail_url=thumbanail_url,
                playlist_id=playlist_id
            )
        )
    return music_items, data["header"][
        "musicHeaderRenderer"]["title"]["runs"][0]["text"]


def extract_search_suggestions(data: Dict) -> List[str]:
    search_suggestions_section: Dict = data["contents"][0][
        "searchSuggestionsSectionRenderer"]
    if "contents" in search_suggestions_section:
        contents = search_suggestions_section["contents"]
    else:
        contents: List[Dict] = search_suggestions_section["shelfDivider"]
    return [
        el["searchSuggestionRenderer"]["navigationEndpoint"][
            "searchEndpoint"]["query"]
        for el in contents
    ]

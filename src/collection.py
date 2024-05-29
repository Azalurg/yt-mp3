from pytube import YouTube


def find_it(soure: dict, key: str):
    if key in soure:
        return soure[key]
    for k, v in soure.items():
        if isinstance(v, dict):
            item = find_it(v, key)
            if item:
                return item
    return None


url = "https://www.youtube.com/watch?v=b1Fo_M_tj6w"
yt = YouTube(url)
data = yt.initial_data
# /engagementPanels/1/engagementPanelSectionListRenderer/content/macroMarkersListRenderer/contents/0/macroMarkersListItemRenderer/thumbnail/thumbnails
chapters = data["engagementPanels"][1]["engagementPanelSectionListRenderer"]["content"][
    "macroMarkersListRenderer"
]["contents"]
for chapter in chapters:
    c = chapter["macroMarkersListItemRenderer"]
    print(c["title"]["simpleText"], find_it(c, "startTimeSeconds") or 0)

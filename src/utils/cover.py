import os

from mutagen.id3 import ID3, APIC


class Cover:
    def __init__(self, directory: str, cover_path: str):
        self.directory = directory
        self.cover_path = cover_path

    def __str__(self):
        return f"Cover: {self.cover_path} in {self.directory}"


def apply_cover(file_path, cover_path) -> int:
    audio_file = ID3(file_path)
    if "APIC" in audio_file:
        del audio_file["APIC"]
    with open(cover_path, "rb") as f:
        audio_file["APIC"] = APIC(
            encoding=3,
            mime="image/jpeg",
            type=3,
            desc="Cover",
            data=f.read(),
        )
    audio_file.save(file_path)
    return 1


def find_covers(path) -> list[Cover]:
    covers = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                covers.append(Cover(root, os.path.join(root, file)))
    return covers


def apply_all_covers(covers: list[Cover]):
    count = 0
    for cover in covers:
        for root, _, files in os.walk(cover.directory):
            for file in files:
                if file.endswith(".mp3"):
                    count += apply_cover(os.path.join(root, file), cover.cover_path)
    print(f"Applied {count} covers")


# TODO: Deal with existing covers (delata/replace)

if __name__ == "__main__":
    print("Applying covers...")
    covers = find_covers("/tmp/music")
    print(f"Found {len(covers)} covers")
    apply_all_covers(covers)
    print("All covers applied!")

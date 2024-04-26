from src.playlist import AgPlaylist

p1 = AgPlaylist(
    "https://www.youtube.com/playlist?list=PLsT9douBcx9_32PkESpk09a-EHwlmF3lN",
    "Powerwolf",
    "Bible of the Beast",
    genre="Power Metal",
    date=2009,
)
p1.download()

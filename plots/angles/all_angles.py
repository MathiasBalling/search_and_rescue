from os import path
from angles import viz_angles
from pathlib import Path


files = {
    "leftnocorner.csv": "Free Space - Can Left",
    "middlenocorner.csv": "Free Space - Can Middle",
    "rightnocorner.csv": "Free Space - Can Right",
    "leftwithcorner.csv": "Corner - Can Left",
    "middlewithcorner.csv": "Corner - Can Middle",
    "rightwithcorner.csv": "Corner - Can Right",
}

DIR = Path(__file__).resolve()

for file in DIR.parent.glob("*.csv"):
    title = path.basename(file).split(".")[0]
    if file.name in files:
        title = files[file.name]
    viz_angles(file.as_posix(), title=f"Angles in {title}", show=False, save=True)

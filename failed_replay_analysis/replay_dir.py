import os
import csv
from pathlib import Path
import ntpath

"""filename: name of csv file, without extension"""


def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([100] * 7)
        filewriter.writerow([200] * 7)


"""replay: path to a replay file"""
"""out_dir: path to the dir to put the csv file in"""


def analyze(replay, out_dir):
    out_file = os.path.join(out_dir, ntpath.basename(os.path.splitext(replay)[0]) + ".csv")
    """data is a 2d matrix- 
        x-coord: time
        y-coord: feature snapshot"""
    data = 0
    write_to_csv(out_file, data)


def main():
    direc = Path('C:/Program Files (x86)/StarCraft II/Replays/Multiplayer')
    replays = []
    for x in direc.iterdir():
        if x.is_file():
            replays.append(x)
    out_dir = Path('C:/Users/Cazamere/Desktop/replay_data')
    analyze(replays[0], out_dir)

main()

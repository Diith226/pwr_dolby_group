import argparse
import os
from pathlib import Path

import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('path')

args = parser.parse_args()

path = Path(args.path)


for i in range(10):
    all_folders_and_files = list(sorted(path.rglob("*"), key=lambda x: len(x.as_posix())))
    for f in tqdm.tqdm(all_folders_and_files):
        try:
            cur_name = f.as_posix()
            new_name = (path / cur_name[len(args.path):].lower()).as_posix()
            os.rename(cur_name, new_name)
        except FileNotFoundError:
            continue

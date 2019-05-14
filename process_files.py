import argparse
import itertools
from pathlib import Path

import h5py
import librosa
import numpy as np
import tqdm

import constants


def convert_single_folder(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    ids = [folder for folder in input_dir.glob("*") if folder.is_dir()]
    all_flacs = list(input_dir.rglob("*.flac"))

    with tqdm.tqdm(total=len(all_flacs)) as pbar:
        for an_id in tqdm.tqdm(ids):
            flacs = list(an_id.rglob("*.flac"))
            speaker_out_dir = output_dir / an_id.name
            speaker_out_dir.mkdir(exist_ok=True, parents=True)

            for flac in flacs:
                audio = librosa.load(flac.as_posix(), sr=constants.LIBRISPEECH_SAMPLE_RATE)[0]
                np.save(speaker_out_dir / flac.with_suffix(".npy").name, audio)
                pbar.update(1)


def convert_single_folder_to_h5(output_file: Path, *input_dirs: Path):
    all_files = itertools.chain.from_iterable(input_dir.glob("*") for input_dir in input_dirs)
    ids = [folder for folder in all_files if folder.is_dir()]
    all_flacs = list(itertools.chain.from_iterable(input_dir.rglob("*.flac") for input_dir in ids))
    dt = h5py.special_dtype(vlen=np.dtype('float32'))

    with h5py.File(output_file.as_posix(), mode="a") as h5_file:
        h5_audio = h5_file.create_dataset("audio", (len(all_flacs),), dtype=dt)
        h5_ids = h5_file.create_dataset("ids", (len(all_flacs),), dtype=np.int32)
        i = 0
        with tqdm.tqdm(total=len(all_flacs)) as pbar:
            for an_id in tqdm.tqdm(ids):
                flacs = list(an_id.rglob("*.flac"))
                for flac in flacs:
                    audio = librosa.load(flac.as_posix(), sr=constants.LIBRISPEECH_SAMPLE_RATE)[0]
                    h5_audio[i] = audio
                    h5_ids[i] = int(flac.parent.parent.name)
                    i += 1
                    pbar.update(1)


def convert_files_to_pickles_h5(input_dir: Path, output_dir: Path):
    convert_single_folder_to_h5(
        output_dir / "train.h5",
        input_dir / "train-clean-100",
        input_dir / "dev-clean",
    )

    convert_single_folder_to_h5(
        output_dir / "test.h5",
        input_dir / "test-clean",
    )


def convert_files_to_pickles(input_dir: Path, output_dir: Path):
    convert_single_folder(input_dir / "train-clean-100", output_dir / "train")
    convert_single_folder(input_dir / "dev-clean", output_dir / "train")
    convert_single_folder(input_dir / "test-clean", output_dir / "test")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")

    args = parser.parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    convert_files_to_pickles(input_dir, output_dir)


if __name__ == '__main__':
    main()

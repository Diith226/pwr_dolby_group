from pathlib import Path
from typing import Callable, List, Optional, Tuple

import librosa
import numpy as np
import pandas as pd
from torch.utils.data import Dataset

import constants


class ExtractStft(object):
    def __init__(self, n_fft: int, hop_length: int, window_size: int):
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.window_size = window_size

    def __call__(self, flac: np.ndarray) -> np.ndarray:
        stft, _, _ = ExtractStft.get_stft(flac, n_fft=self.n_fft, hop_length=self.hop_length,
                                          window_size=self.window_size)
        return stft

    @staticmethod
    def get_stft(flac: np.ndarray, *,
                 n_fft: int = 512,
                 hop_length: int = 128,
                 window_size: int = 512) -> Tuple[np.ndarray, np.ndarray, float]:
        fouriered = librosa.stft(flac, n_fft=n_fft, hop_length=hop_length, win_length=window_size, center=True)

        mag, phase = librosa.magphase(fouriered)
        mag = np.power(mag, constants.MAGNITUDE_NONLINEARITY)
        mag_max_value = mag.max()

        mag = (1 - mag / mag.max()) * 255 - 127.5
        return np.flipud(mag).copy()[..., np.newaxis], phase, mag_max_value


class RandomCrop(object):
    def __init__(self, crop_width: int, seed: Optional[int] = None):
        self.crop_width = crop_width
        self._rng = np.random.RandomState(seed)

    def __call__(self, spectogram: np.ndarray) -> np.ndarray:
        width = spectogram.shape[1]
        index = self._rng.randint(0, width - self.crop_width)
        return spectogram[:, index:index + self.crop_width]


class LibriSpeechDataset(Dataset):
    def __init__(self, npy_files: List[Path], speakers_info_path: str,
                 transforms: Optional[Callable] = None):
        self._npy_files = npy_files
        self._speakers_data = pd.read_csv(speakers_info_path, delimiter="|",
                                          comment=";", header=None)
        self._speakers_data.columns = ["id", "sex", "dataset", "minutes", "name"]
        self._speakers_data["sex"] = self._speakers_data["sex"].map(str.strip)

        self._id_to_sex_map = {}
        self._sex_to_class = {
            "F": 0,
            "M": 1
        }
        self._speakers_data.apply(lambda row: self._id_to_sex_map.update({
            row["id"]: row["sex"]
        }), axis=1)

        self.transforms = transforms

    def __getitem__(self, index):
        audio_data = np.load(self._npy_files[index])
        speaker_id = int(self._npy_files[index].parent.name)

        if self.transforms is not None:
            audio_data = self.transforms(audio_data)

        sex = self._id_to_sex_map.get(speaker_id, "F")
        a_class = self._sex_to_class[sex]
        audio_data = np.transpose(audio_data, (2, 0, 1))

        return audio_data, a_class

    def __len__(self):
        return len(self._npy_files)

from pathlib import Path
from typing import NamedTuple

CONSTANTS_FILE_PATH = Path(__file__).parent.absolute()

LIBRISPEECH_SAMPLE_RATE = 44100
EPSILON = 1e-8
STFT_CROP_WIDTH = 64

SPEAKER_DATA_PATH = "data/processed/LibriSpeech/SPEAKERS.TXT"

NUMBER_OF_CLASSES = 2  # female, male

MAGNITUDE_NONLINEARITY = 1 / 8


class AudioParams(NamedTuple):
    model_path: Path
    components: int
    hop_length: int
    window_size: int


AUDIO_PARAMS_SLOWER_BETTER_MODEL = AudioParams(CONSTANTS_FILE_PATH / "models" / "slower_better_model" / "params.pt",
                                               2048, 256, 2048)
AUDIO_PARAMS_FASTER_WORSE_MODEL = AudioParams(CONSTANTS_FILE_PATH / "models" / "faster_worse_model" / "params.pt",
                                              512, 512 // 4, 512)

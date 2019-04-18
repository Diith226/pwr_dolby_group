import os
from functools import partial
from typing import Iterable, Optional, Tuple, Union

import cv2
import librosa
import numpy as np
import torch
import torch.nn as nn
import tqdm
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from skorch.net import NeuralNet

import constants
from dataset import ExtractStft
from model import Classifier
from pytorch_extensions import roll


class DataLoader(TransformerMixin, BaseEstimator):
    def fit(self, x, y, **fit_params):
        return self

    @classmethod
    def transform(cls, x: Iterable[str]) -> Iterable[Tuple[np.ndarray, int]]:
        output = []
        for file_name in x:
            signal, sample_rate = librosa.load(file_name, sr=constants.LIBRISPEECH_SAMPLE_RATE)
            output.append((signal, sample_rate))
        return output


class DataPreprocessor(TransformerMixin, BaseEstimator):
    def fit(self, x, y, **fit_params):
        return self

    @classmethod
    def transform(cls, x: Iterable[Tuple[np.ndarray, int]]) -> Iterable[Tuple[np.ndarray, int, float, np.ndarray]]:
        output = []
        for signal, sample_rate in x:
            stacked, original_phase, max_value = ExtractStft.get_stft(signal)
            output.append((stacked, sample_rate, max_value, original_phase))
        return output


class Model(TransformerMixin, BaseEstimator):
    def __init__(self,
                 model_path: str,
                 block_name: str,
                 number_of_iterations: int,
                 optimisation_step_size: float = 1.5,
                 n_octaves: int = 4,
                 octave_scale: float = 1.4,
                 use_gpu: bool = False,
                 verbose: bool = False,
                 seed: Optional[int] = None):
        self._model_path = model_path
        self._use_gpu = use_gpu
        self._block_name = block_name
        self._n_octaves = n_octaves
        self._octave_scale = octave_scale
        self._verbose = verbose
        self._number_of_iterations = number_of_iterations
        self._np_rng = np.random.RandomState(seed)
        self._optimisation_step_size = optimisation_step_size

        self._available_layers = {}
        self._available_layers_names = []

        self._classifier = Classifier(constants.NUMBER_OF_CLASSES)
        self._net = NeuralNet(
            self._classifier, nn.CrossEntropyLoss
        )
        self._net.initialize()
        self._net.load_params(f_params=self._model_path)

        for layer_name, layer in self._classifier.layers_blocks.items():
            if "residual" in layer_name:
                current_register = partial(self._register_layer_output, layer_name=layer_name)
                layer.register_forward_hook(current_register)
                self._available_layers_names.append(layer_name)

        if self._verbose:
            print(f"Available layer names: \n{self._available_layers_names}")

    def _register_layer_output(self, module, input_, output, layer_name):
        self._available_layers[layer_name] = output

    def fit(self, x, y, **fit_params):
        return self

    def transform(self,
                  x: Iterable[Tuple[np.ndarray, int, float, np.ndarray]]
                  ) -> Iterable[Tuple[np.ndarray, int, float, np.ndarray]]:
        output = []
        for stft, sample_rate, max_value, original_phase in x:
            prediction = self._transform_single_normal_deep_dream(stft)
            output.append((prediction, sample_rate, max_value, original_phase))
        return output

    def _transform_single_normal_deep_dream(self, stft: np.ndarray) -> np.ndarray:
        octaves = []
        for i in range(self._n_octaves - 1):
            hw = stft.shape[:-1]
            lo = self.resize_stft(stft, np.int32(np.float32(hw) / self._octave_scale))
            hi = stft - self.resize_stft(lo, hw)
            stft = lo
            octaves.append(hi)

        for octave in tqdm.trange(self._n_octaves, desc="Image optimisation", disable=not self._verbose):
            if octave > 0:
                hi = octaves[-octave]
                stft = self.resize_stft(stft, hi.shape[:-1]) + hi

            stft = torch.from_numpy(stft).float().contiguous()
            if self._use_gpu:
                stft = stft.cuda()
            stft = stft.permute((2, 0, 1))

            for i in tqdm.trange(self._number_of_iterations, desc="Octave optimisation",
                                 disable=not self._verbose):
                g = self.calc_grad_tiled(stft)
                stft += g * (self._optimisation_step_size / (g.pow(2).mean().pow(1 / 2) + 1e-7))

            stft = stft.cpu().numpy().transpose((1, 2, 0))

        stft[..., 0] = stft[..., 0] / stft[..., 0].max() - constants.DATA_MEANS[0]
        stft[..., 1] = stft[..., 1] / stft[..., 1].max() - constants.DATA_MEANS[1]
        return stft

    def calc_grad_tiled(self, stft: torch.Tensor, tile_size: int = 128) -> torch.Tensor:
        h, w = stft.shape[1:]
        sx, sy = self._np_rng.randint(5, size=2)
        stft_shift = roll(roll(stft, sx, axis=2), sy, axis=1)
        grads = torch.zeros_like(stft)
        for y in range(0, max(h - tile_size // 2, tile_size), tile_size):
            for x in range(0, max(w - tile_size // 2, tile_size), tile_size):
                frame = stft_shift[:, y:y + tile_size, x:x + tile_size]
                frame.requires_grad = True
                self._classifier(frame[None])

                # 16 is a filter to optimise, arbitrary number in range 0 - 255 can be chosen
                layer_output = self._available_layers[self._block_name][0, 16]
                objective_output = self._objective(layer_output)
                objective_output.backward()

                frame.requires_grad = False
                grad = frame.grad.detach().clone()
                grads[:, y:y + tile_size, x:x + tile_size] = grad
        result = roll(roll(grads, -sx, axis=2), -sy, axis=1)
        return result

    @classmethod
    def _objective(cls, data: torch.Tensor) -> torch.Tensor:
        return data.mean()

    @classmethod
    def resize_stft(cls, stft: np.ndarray, hw_desired_size: Union[Tuple, np.ndarray]) -> np.ndarray:
        mag = cv2.resize(stft[..., 0], tuple(hw_desired_size[::-1]))
        phase = cv2.resize(stft[..., 1], tuple(hw_desired_size[::-1]))
        return np.stack((mag, phase), axis=-1)


class Denormalize(TransformerMixin, BaseEstimator):
    def fit(self, x, y=None, **fit_params):
        return self

    @classmethod
    def transform(cls, x: Iterable[Tuple[np.ndarray, int, float, np.ndarray]]) -> Iterable[Tuple[np.ndarray, int]]:
        output = []
        for stft, fs, max_value, original_phase in x:
            stft = np.flipud(stft)
            mag, _ = np.split(stft, 2, axis=-1)
            mag = mag[..., 0]

            mag = (1 - ((mag + constants.DATA_MEANS[0]) / 2 + 0.5)) * max_value
            mag = np.power(mag, 1 / constants.MAGNITUDE_NONLINEARITY)

            stft = mag * original_phase
            unfouriered = librosa.istft(stft, win_length=constants.LIBRISPEECH_WINDOW_SIZE)
            output.append((unfouriered, fs))
        return output


class SaveResult(TransformerMixin, BaseEstimator):
    def __init__(self, output_dir: str, base_name: str):
        self.output_dir = output_dir
        self.base_name = base_name

    def fit(self, x, y=None, **fit_params):
        return self

    def transform(self, x: Iterable[Tuple[np.ndarray, int]]) -> Iterable[Tuple[np.ndarray, int]]:
        output = []
        for i, (signal, fs) in enumerate(x):
            path = os.path.join(self.output_dir, self.base_name + "_{}.wav".format(i))
            librosa.output.write_wav(path, signal, fs)
            output.append((signal, fs))
        return output


def get_processing_pipeline(model_path: str, *, n_octaves: int = 8, number_of_iterations: int = 10,
                            optimisation_step_size: float = 0.5) -> Pipeline:
    return Pipeline([
        ("data load", DataLoader()),
        ("data processor", DataPreprocessor()),
        ("deep dream", Model(
            block_name="residual_5a",
            model_path=model_path,
            n_octaves=n_octaves,
            number_of_iterations=number_of_iterations,
            optimisation_step_size=optimisation_step_size,
            verbose=True,
            use_gpu=False,
        )),
        ("denormalize", Denormalize()),
        ("data saver", SaveResult(".", "audio"))
    ])


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", help="Path to model")
    parser.add_argument("file_path", help="Path to .wav file to process")
    args = parser.parse_args()

    pipe = get_processing_pipeline(args.model_path)
    print(pipe.transform([args.file_path]))


if __name__ == '__main__':
    main()

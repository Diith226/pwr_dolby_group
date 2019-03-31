import os
from functools import partial
from pathlib import Path
from typing import *

import numpy as np
import scipy.ndimage as nd
import soundfile as sf
import torch
import torch.nn as nn
import torch.optim
import tqdm
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from torch.autograd import Variable

import constants
from data_io import read_conf_inp, str_to_bool
from dnn_models import MLP
from dnn_models import SincNet as CNN
from pytorch_extensions import roll, pad1d

cfg_file = Path("cfg") / "SincNet_TIMIT.cfg"  # Config file of the speaker-id experiment used to generate the model
energy_threshold = 0.1  # Avoid frames with an energy that is 1/10 over the average energy

# Reading cfg file
options = read_conf_inp(cfg_file)

# [windowing]
sampling_rate = int(options.fs)
config_window_length = int(options.cw_len)
config_window_shift = int(options.cw_shift)

# [cnn]
cnn_N_filt = list(map(int, options.cnn_N_filt.split(',')))
cnn_len_filt = list(map(int, options.cnn_len_filt.split(',')))
cnn_max_pool_len = list(map(int, options.cnn_max_pool_len.split(',')))
cnn_use_laynorm_inp = str_to_bool(options.cnn_use_laynorm_inp)
cnn_use_batchnorm_inp = str_to_bool(options.cnn_use_batchnorm_inp)
cnn_use_laynorm = list(map(str_to_bool, options.cnn_use_laynorm.split(',')))
cnn_use_batchnorm = list(map(str_to_bool, options.cnn_use_batchnorm.split(',')))
cnn_act = list(map(str, options.cnn_act.split(',')))
cnn_drop = list(map(float, options.cnn_drop.split(',')))

# [dnn]
fc_layer_sizes = list(map(int, options.fc_lay.split(',')))
fc_drop = list(map(float, options.fc_drop.split(',')))
fc_use_laynorm_inp = str_to_bool(options.fc_use_laynorm_inp)
fc_use_batchnorm_inp = str_to_bool(options.fc_use_batchnorm_inp)
fc_use_batchnorm = list(map(str_to_bool, options.fc_use_batchnorm.split(',')))
fc_use_laynorm = list(map(str_to_bool, options.fc_use_laynorm.split(',')))
fc_act = list(map(str, options.fc_act.split(',')))

# Converting context and shift in samples
window_length = int(sampling_rate * config_window_length / 1000.00)
window_shift = int(sampling_rate * config_window_shift / 1000.00)


class DataLoader(TransformerMixin, BaseEstimator):
    def fit(self, x, y, **fit_params):
        return self

    @classmethod
    def transform(cls, x: Iterable[str]) -> Iterable[Tuple[np.ndarray, int]]:
        output = []
        for file_name in x:
            signal, sample_rate = sf.read(file_name)
            output.append((signal, sample_rate))
        return output


class DataPreprocessor(TransformerMixin, BaseEstimator):
    def fit(self, x, y, **fit_params):
        return self

    @classmethod
    def transform(cls, x: Iterable[Tuple[np.ndarray, int]]) -> Iterable[Tuple[np.ndarray, int, float]]:
        output = []
        for signal, sample_rate in x:
            # Amplitude normalization
            max_value = np.max(np.abs(signal))
            signal = signal / max_value
            output.append((signal, sample_rate, max_value))
        return output


class DeepDream(TransformerMixin, BaseEstimator):
    def __init__(self,
                 model_path: str,
                 *,
                 layer_name: str = constants.DEFAULT_LAYER,
                 step_size: float = constants.DEFAULT_STEP_SIZE,
                 octave_scale: float = constants.DEFAULT_OCTAVE_SCALE,
                 number_of_octaves: int = constants.DEFAULT_NUMBER_OF_OCTAVES,
                 number_of_iterations: int = constants.DEFAULT_NUMBER_OF_ITERATIONS,
                 number_of_chunks: int = constants.DEFAULT_NUMBER_OF_CHUNKS,
                 clip_values: bool = True,
                 use_gpu: bool = False,
                 verbose: bool = False,
                 jitter: int = 512,
                 random_state: Optional[int] = None):
        self._cnn_net: Optional[nn.Module] = None
        self._dnn_net: Optional[nn.Module] = None
        self._available_layers: Dict[str, torch.Tensor] = {}
        self._available_layer_names: List[str] = []

        self.layer_name = layer_name
        self.verbose = verbose
        self.number_of_chunks = number_of_chunks
        self.layer_name = layer_name
        self.use_gpu = use_gpu
        self.jitter = jitter
        self.step_size = step_size
        self.number_of_iterations = number_of_iterations
        self.number_of_octaves = number_of_octaves
        self.octave_scale = octave_scale
        self.clip_values = clip_values

        self._np_rng = np.random.RandomState(random_state)

        if self.verbose:
            print("Loading model ...")

        self._load_model(model_path)

        if self.verbose:
            print(f"Loaded model. Available layers are: {self._available_layer_names}")

    def fit(self, x, y, **fit_params):
        return self

    def _register_layer_output(self, module, input_, output, layer_name):
        self._available_layers[layer_name] = output

    def _load_model(self, model_path: str):
        cnn_arch = {'input_dim': window_length,
                    'fs': sampling_rate,
                    'cnn_N_filt': cnn_N_filt,
                    'cnn_len_filt': cnn_len_filt,
                    'cnn_max_pool_len': cnn_max_pool_len,
                    'cnn_use_laynorm_inp': cnn_use_laynorm_inp,
                    'cnn_use_batchnorm_inp': cnn_use_batchnorm_inp,
                    'cnn_use_laynorm': cnn_use_laynorm,
                    'cnn_use_batchnorm': cnn_use_batchnorm,
                    'cnn_act': cnn_act,
                    'cnn_drop': cnn_drop,
                    }
        self._cnn_net = CNN(cnn_arch)

        dnn_arch = {'input_dim': self._cnn_net.out_dim,
                    'fc_lay': fc_layer_sizes,
                    'fc_drop': fc_drop,
                    'fc_use_batchnorm': fc_use_batchnorm,
                    'fc_use_laynorm': fc_use_laynorm,
                    'fc_use_laynorm_inp': fc_use_laynorm_inp,
                    'fc_use_batchnorm_inp': fc_use_batchnorm_inp,
                    'fc_act': fc_act,
                    }

        self._dnn_net = MLP(dnn_arch)

        checkpoint_load = torch.load(model_path)
        self._cnn_net.load_state_dict(checkpoint_load['CNN_model_par'])
        self._dnn_net.load_state_dict(checkpoint_load['DNN1_model_par'])

        self._cnn_net.eval()
        self._dnn_net.eval()

        for i, layer in enumerate(self._cnn_net.act):
            layer_name = f"conv_{i}"
            current_register = partial(self._register_layer_output, layer_name=layer_name)
            self._available_layer_names.append(layer_name)
            layer.register_forward_hook(current_register)

        for i, layer in enumerate(self._dnn_net.act):
            layer_name = f"dense_{i}"
            current_register = partial(self._register_layer_output, layer_name=layer_name)
            self._available_layer_names.append(layer_name)
            layer.register_forward_hook(current_register)

        if self.use_gpu:
            self._cnn_net.cuda()
            self._dnn_net.cuda()

    def transform(self, x: Iterable[Tuple[np.ndarray, int, float]]) -> Iterable[Tuple[np.ndarray, int, float]]:
        output = []
        for signal, sample_rate, max_value in x:
            prediction = self._transform_single(signal)
            output.append((prediction, sample_rate, max_value))
        return output

    def _transform_single(self, signal: np.ndarray) -> np.ndarray:
        signal = torch.from_numpy(signal).contiguous().float()
        if self.use_gpu:
            signal = signal.gpu()
        octaves = [signal]
        for i in range(self.number_of_octaves - 1):
            new_octave = nd.zoom(octaves[-1], 1 / self.octave_scale, order=2)
            new_octave = torch.from_numpy(new_octave).contiguous().float()
            if self.use_gpu:
                new_octave = new_octave.cuda()
            octaves.append(new_octave)

        detail = torch.zeros_like(octaves[-1]).contiguous().float()
        if self.use_gpu:
            detail = detail.cuda()
        output_data = signal
        for octave, octave_base in enumerate(octaves[::-1]):
            if self.verbose:
                print(f"Trying octave: {octave + 1} / {len(octaves)}")
            length = octave_base.shape[-1]
            if octave > 0:
                rescaled_detail = nd.zoom(detail, length / len(detail), order=2)
                detail = torch.from_numpy(rescaled_detail).contiguous().float()
                if self.use_gpu:
                    detail = detail.cuda()

            octave_base, detail = self._match_to_longer_sequence(octave_base, detail)

            output_data = octave_base + detail
            for _ in tqdm.tqdm(range(self.number_of_iterations), total=self.number_of_iterations,
                               disable=not self.verbose):
                output_data = self._make_step(output_data)
                if self.clip_values:
                    output_data = torch.clamp(output_data, -1, 1)

            detail = output_data - octave_base

        return output_data

    def _make_step(self, signal: torch.Tensor) -> torch.Tensor:
        random_shift = self._np_rng.randint(-self.jitter, self.jitter + 1)
        signal = roll(signal, random_shift, 0)
        frames = self._generate_frames(signal)
        grads = torch.zeros_like(frames)

        optimizer = torch.optim.Adadelta(list(self._dnn_net.parameters()) + list(self._cnn_net.parameters()))

        for i in range(0, len(frames), self.number_of_chunks):
            start_index = i
            end_index = min(i + self.number_of_chunks, len(frames))
            batch = frames[start_index:end_index]

            network_input = Variable(batch)
            network_input.requires_grad = True

            optimizer.zero_grad()

            self._dnn_net(self._cnn_net(network_input))
            layer_output = self._available_layers[self.layer_name]
            layer_output = self._objective(layer_output)
            layer_output.backward()

            batch_grad = network_input.grad.detach()

            grads[start_index:end_index] = batch_grad
        full_grad = self._restore_signal_shape(frames, signal)
        signal += self.step_size / torch.abs(full_grad).mean() * full_grad
        signal = roll(signal, -random_shift, 0)
        return signal

    @classmethod
    def _match_to_longer_sequence(cls, first: torch.Tensor, second: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        first_length = len(first)
        second_length = len(second)

        first_pad = second_length - first_length if second_length > first_length else 0
        second_pad = first_length - second_length if first_length > second_length else 0

        first = pad1d(first, (0, first_pad))
        second = pad1d(second, (0, second_pad))
        return first, second

    @classmethod
    def _objective(cls, data: torch.Tensor) -> torch.Tensor:
        return torch.sqrt(data.pow(2).sum())

    def _generate_frames(self, signal: torch.Tensor) -> torch.Tensor:
        # split signals into chunks
        number_of_frames = int((signal.shape[0] - window_length) / window_shift + 1)
        frames = torch.zeros([number_of_frames, window_length]).float().contiguous()

        if self.use_gpu:
            frames = frames.cuda()

        beginning_of_sample = 0
        end_of_sample = window_length
        frame_count = 0

        while end_of_sample < signal.shape[0]:
            frames[frame_count, :] = signal[beginning_of_sample:end_of_sample]
            beginning_of_sample = beginning_of_sample + window_shift
            end_of_sample = beginning_of_sample + window_length
            frame_count = frame_count + 1
        return frames

    @classmethod
    def _restore_signal_shape(cls, frames: torch.Tensor, original_signal: torch.Tensor) -> torch.Tensor:
        restored_signal = torch.zeros_like(original_signal)
        offset = 0
        previous_ending_offset = -1
        for frame in frames:
            input_slice = slice(offset, offset + window_length)
            restored_signal[input_slice] = frame

            if previous_ending_offset > 0:
                overlap_slice = slice(offset, previous_ending_offset)
                restored_signal[overlap_slice] /= 2

            previous_ending_offset = input_slice.stop
            offset += window_shift
        return restored_signal


class Denormalize(TransformerMixin, BaseEstimator):
    def fit(self, x, y=None, **fit_params):
        return self

    @classmethod
    def transform(cls, x: Iterable[Tuple[np.ndarray, int, float]]) -> Iterable[Tuple[np.ndarray, int]]:
        output = []
        for signal, fs, max_value in x:
            signal *= max_value
            output.append((signal, fs))
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
            sf.write(path, signal, fs)
            output.append((signal, fs))
        return output


def get_processing_pipeline(model_path: str) -> Pipeline:
    return Pipeline([
        ("data load", DataLoader()),
        ("data processor", DataPreprocessor()),
        ("deep dream", DeepDream(
            layer_name="dense_1",
            model_path=model_path,
            number_of_octaves=1,
            step_size=0.5,
            jitter=2048,
            verbose=True,
            use_gpu=False
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

from pathlib import Path
from typing import *

import numpy as np
import soundfile as sf
import torch
import torch.nn as nn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from torch.autograd import Variable

from data_io import read_conf_inp, str_to_bool
from dnn_models import MLP
from dnn_models import SincNet as CNN

cfg_file = Path("cfg") / "SincNet_TIMIT.cfg"  # Config file of the speaker-id experiment used to generate the model
energy_threshold = 0.1  # Avoid frames with an energy that is 1/10 over the average energy

use_cuda = torch.cuda.is_available()

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
    def transform(cls, x: Iterable[str]) -> Iterable[Tuple[np.ndarray, float]]:
        output = []
        for file_name in x:
            signal, sample_rate = sf.read(file_name)

            # Amplitude normalization
            signal = signal / np.max(np.abs(signal))
            output.append((signal, sample_rate))
        return output


class DeepDream(TransformerMixin, BaseEstimator):
    def __init__(self, model_path: str, number_of_chunks: int, verbose: bool = False):
        self.cnn_net: Optional[nn.Module] = None
        self.dnn_net: Optional[nn.Module] = None

        self.verbose = verbose
        self.number_of_chunks = number_of_chunks

        if self.verbose:
            print("Loading model ...")
        self.load_model(model_path)

    def fit(self, x, y, **fit_params):
        return self

    def load_model(self, model_path: str):
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
        self.cnn_net = CNN(cnn_arch)

        dnn_arch = {'input_dim': self.cnn_net.out_dim,
                    'fc_lay': fc_layer_sizes,
                    'fc_drop': fc_drop,
                    'fc_use_batchnorm': fc_use_batchnorm,
                    'fc_use_laynorm': fc_use_laynorm,
                    'fc_use_laynorm_inp': fc_use_laynorm_inp,
                    'fc_use_batchnorm_inp': fc_use_batchnorm_inp,
                    'fc_act': fc_act,
                    }

        self.dnn_net = MLP(dnn_arch)

        checkpoint_load = torch.load(model_path)
        self.cnn_net.load_state_dict(checkpoint_load['CNN_model_par'])
        self.dnn_net.load_state_dict(checkpoint_load['DNN1_model_par'])

        self.cnn_net.eval()
        self.dnn_net.eval()

        if use_cuda:
            self.cnn_net.cuda()
            self.dnn_net.cuda()

    def transform(self, x: Iterable[Tuple[np.ndarray, float]]) -> Iterable[Tuple[Optional[np.ndarray], float]]:
        with torch.no_grad():
            output = []
            for signal, sample_rate in x:
                signal = torch.from_numpy(signal).float().contiguous()
                if use_cuda:
                    signal = signal.cuda()

                # split signals into chunks
                beginning_of_sample = 0
                end_of_sample = window_length

                number_of_frames = int((signal.shape[0] - window_length) / window_shift + 1)
                signal_array = torch.zeros([self.number_of_chunks, window_length]).float().contiguous()

                vector_dim = fc_layer_sizes[-1]
                vectors = Variable(torch.zeros(number_of_frames, vector_dim).float().contiguous())

                if use_cuda:
                    signal_array = signal_array.cuda()
                    vectors = vectors.cuda()

                frame_count = 0
                vectors_output_offset = 0

                while end_of_sample < signal.shape[0]:
                    signal_array[frame_count, :] = signal[beginning_of_sample:end_of_sample]
                    beginning_of_sample = beginning_of_sample + window_shift
                    end_of_sample = beginning_of_sample + window_length
                    frame_count = frame_count + 1

                    if frame_count == self.number_of_chunks:
                        network_input = Variable(signal_array)

                        vectors[vectors_output_offset:vectors_output_offset + len(signal_array)] = \
                            self.dnn_net(self.cnn_net(network_input))

                        vectors_output_offset += len(signal_array)
                        frame_count = 0

                        signal_array = torch.zeros([self.number_of_chunks, window_length]).float().contiguous()
                        if use_cuda:
                            signal_array = signal_array.cuda()

                if frame_count > 0:
                    network_input = Variable(signal_array[:frame_count])
                    vectors[vectors_output_offset:] = \
                        self.dnn_net(self.cnn_net(network_input))

                # averaging and normalizing all the d-vectors
                predictions = torch.mean(vectors / vectors.norm(p=2, dim=1).view(-1, 1), dim=0)
                if use_cuda:
                    predictions = predictions.cpu()

                # checks for nan
                nan_sum = torch.sum(torch.isnan(predictions))

            if nan_sum > 0:
                print("NaNs occurred, no result is returned")
                output.append((None, sample_rate))
            else:
                output.append((predictions.numpy(), sample_rate))
        return output


def get_processing_pipeline(model_path: str) -> Pipeline:
    return Pipeline([
        ("data load", DataLoader()),
        ("deep dream", DeepDream(model_path, 128))
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

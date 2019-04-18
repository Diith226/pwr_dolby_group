import argparse
from pathlib import Path

import numpy as np
import torch
import tqdm
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from skorch import NeuralNet
from skorch.callbacks import Checkpoint, EarlyStopping, ProgressBar, EpochScoring
from skorch.helper import predefined_split
from torch.utils.data import Dataset
from torchvision.transforms import Compose

import constants
from callbacks import Tensorboard
from dataset import LibriSpeechDataset, ExtractStft, RandomCrop
from model import Classifier


# Needed it because of in `DataLoader` for validation set
# RuntimeError: received 0 items of ancdata
# https://github.com/pytorch/pytorch/issues/973#issuecomment-426559250
torch.multiprocessing.set_sharing_strategy('file_system')


def acc_as_metric(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    return (np.argmax(y_pred, axis=1) == y_true).mean().item()


def acc(net: NeuralNet, ds: Dataset, y: torch.Tensor) -> float:
    predict_values = net.predict(ds)
    return acc_as_metric(predict_values, y)


def train(data_folder: str, out_model: str):
    out_model = Path(out_model)
    out_model.mkdir()

    data_paths = list(Path(data_folder).rglob("*.npy"))
    train_paths, valid_paths = train_test_split(data_paths, train_size=0.7)

    train_dataset = LibriSpeechDataset(train_paths, Path(data_folder).parent / "SPEAKERS.TXT", Compose([
        ExtractStft(), RandomCrop(constants.STFT_CROP_WIDTH)
    ]))

    valid_dataset = LibriSpeechDataset(valid_paths, Path(data_folder).parent / "SPEAKERS.TXT", Compose([
        ExtractStft(), RandomCrop(constants.STFT_CROP_WIDTH)
    ]))

    net = NeuralNet(
        Classifier,
        module__n_classes=constants.NUMBER_OF_CLASSES,
        criterion=nn.CrossEntropyLoss,
        batch_size=8,
        max_epochs=100,
        optimizer=optim.Adam,
        lr=0.001,
        iterator_train__shuffle=True,
        iterator_train__num_workers=2,
        iterator_valid__shuffle=False,
        iterator_valid__num_workers=2,
        train_split=predefined_split(valid_dataset),
        device="cuda",
        callbacks=[
            Checkpoint(
                f_params=(out_model / "params.pt").as_posix(),
                f_optimizer=(out_model / "optim.pt").as_posix(),
                f_history=(out_model / "history.pt").as_posix()
            ),
            ProgressBar(postfix_keys=["train_loss", "train_acc"]),
            EarlyStopping(),
            EpochScoring(acc, name="val_acc", lower_is_better=False, on_train=False),
            EpochScoring(acc, name="train_acc", lower_is_better=False, on_train=True),
            Tensorboard((out_model / "train").as_posix(), metrics={"acc": acc_as_metric}, is_training=True),
            Tensorboard((out_model / "valid").as_posix(), metrics={"acc": acc_as_metric}, is_training=False),
        ]
    )

    net.fit(train_dataset)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_folder")
    parser.add_argument("--out_model")

    args = parser.parse_args()
    train(args.data_folder, args.out_model)


if __name__ == '__main__':
    main()

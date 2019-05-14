from typing import Dict, Callable, Optional

import torch
from skorch.callbacks import Callback
from tensorboardX import SummaryWriter


class Tensorboard(Callback):
    def __init__(self, save_path: str, metrics: Dict[str, Callable], is_training: bool):
        self._save_path = save_path
        self._metrics = metrics
        self._is_training = is_training

        self._writer: Optional[SummaryWriter] = None
        self._step = 0

    def _initialize_cache(self):
        self.y_trues_ = []
        self.y_preds_ = []

    def initialize(self):
        self._writer = SummaryWriter(self._save_path)
        self._step = 0
        self._initialize_cache()
        super().initialize()

    # pylint: disable=arguments-differ
    def on_batch_end(self, net, y, y_pred, training, **kwargs):
        self.y_trues_.append(y)
        self.y_preds_.append(y_pred)
        if self._is_training and training:
            trues = torch.cat(tuple(self.y_trues_), dim=0)
            preds = torch.cat(tuple(self.y_preds_), dim=0)
            for name, metric in self._metrics.items():
                self._writer.add_scalar(name, metric(preds.detach().cpu().numpy(), trues.detach().cpu().numpy()),
                                        global_step=self._step)

        self._step += 1

    def on_epoch_end(self, net,
                     dataset_train=None, dataset_valid=None, **kwargs):
        if not self._is_training:
            trues = torch.cat(tuple(self.y_trues_), dim=0)
            preds = torch.cat(tuple(self.y_preds_), dim=0)
            for name, metric in self._metrics.items():
                self._writer.add_scalar(name, metric(preds.detach().cpu().numpy(), trues.detach().cpu().numpy()),
                                        global_step=self._step)

    def on_train_end(self, net, X=None, y=None, **kwargs):
        self._initialize_cache()
        self._step = 0
        self._writer.close()

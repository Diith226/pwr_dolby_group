from collections import OrderedDict

import numpy as np
import torch.nn as nn
import torch.nn.functional as functional


class ResidualBlock2d(nn.Module):
    def __init__(self, in_filters: int, out_filters: int, kernel_size: int, stride: int):
        super().__init__()

        self.conv_1 = nn.Sequential(OrderedDict((
            ("conv_1", nn.Conv2d(in_filters, in_filters, (kernel_size, kernel_size),
                                 padding=(kernel_size // 2, kernel_size // 2))),
            ("batchnorm_1", nn.BatchNorm2d(in_filters)),
            ("relu_1", nn.ReLU())
        )))

        self.conv_2 = nn.Sequential(OrderedDict((
            ("conv_2", nn.Conv2d(in_filters, out_filters, (kernel_size, kernel_size),
                                 padding=(kernel_size // 2, kernel_size // 2), stride=(stride, stride))),
            ("batchnorm_2", nn.BatchNorm2d(out_filters)),
        )))

        self.out_relu = nn.Sequential(OrderedDict((("relu_2", nn.ReLU()),)))
        self.stride = stride
        self.should_add_input = True

        if stride > 1 or out_filters != in_filters:
            self.linear_transform = nn.Sequential(
                OrderedDict((("conv_input", nn.Conv2d(in_filters, out_filters, (1, 1), stride=(stride, stride))),))
            )
            if stride > 1:
                self.should_add_input = False
        else:
            self.linear_transform = lambda x: x

    def forward(self, inputs):
        x = self.conv_1(inputs)
        x = self.conv_2(x)
        if self.should_add_input:
            x = self.linear_transform(inputs) + x
        return self.out_relu(x)


class Classifier(nn.Module):
    def __init__(self, n_classes: int):
        super().__init__()

        self.layers_blocks = OrderedDict((
            ("residual_1a", ResidualBlock2d(2, 16, 7, 2)),
            ("pool_1", nn.AvgPool2d((2, 2))),
            ("residual_2a", ResidualBlock2d(16, 64, 3, 1)),
            ("residual_2b", ResidualBlock2d(64, 64, 3, 1)),
            ("pool_2", nn.AvgPool2d((2, 2))),
            ("residual_3a", ResidualBlock2d(64, 128, 3, 1)),
            ("residual_3b", ResidualBlock2d(128, 128, 3, 1)),
            ("pool_3", nn.AvgPool2d((2, 2))),
            ("residual_4a", ResidualBlock2d(128, 256, 3, 1)),
            ("residual_4b", ResidualBlock2d(256, 256, 3, 1)),
            ("pool_4", nn.AvgPool2d((2, 2))),
            ("residual_5a", ResidualBlock2d(256, 256, 3, 1)),
            ("residual_5b", ResidualBlock2d(256, 256, 3, 1)),
        ))

        self.layers = nn.Sequential(self.layers_blocks)

        self.classification_part = nn.Sequential(OrderedDict([
            ("classification_1", nn.Linear(256, n_classes))
        ]))

    def forward(self, inputs):
        x = self.layers(inputs)
        n, c, h, w = x.size()
        x = functional.avg_pool2d(x, (h, w)).view(n, c)
        x = self.classification_part(x)
        return x

    @property
    def num_params(self):
        return np.sum(
            [np.prod(param.size()) for param in self.parameters()]
        )


if __name__ == '__main__':
    print(Classifier(2).state_dict().keys())

import torch


def roll(tensor: torch.Tensor, shift: int, axis: int = 0) -> torch.Tensor:
    axes = list(range(len(tensor.shape)))
    axes[0], axes[axis] = axes[axis], axes[0]
    tensor = tensor.permute(axes)
    tensor = torch.cat((tensor[-shift:], tensor[:-shift]), dim=0)
    tensor = tensor.permute(axes)
    return tensor


def pad1d(tensor: torch.Tensor, pad_size: tuple) -> torch.Tensor:
    """
    Needed this because from torch.nn.functional supports only 2D and more D inputs
    :param tensor: torch.Tensor. Tensor to pad.
    :param pad_size: tuple of two ints. Number of points to pad on each side.
    :return: Padded tensor with constant values equal to mean.
    """
    left, right = pad_size
    output = torch.zeros_like(tensor)
    output.fill_(tensor.mean())
    if right > 0:
        output[left:-right] = tensor
    else:
        output[left:] = tensor
    return tensor

# --------------------------------------------------------
# mcan-vqa (Deep Modular Co-Attention Networks)
# Licensed under The MIT License [see LICENSE for details]
# Written by Yuhao Cui https://github.com/cuiyuhao1996
# --------------------------------------------------------

import torch
import torch.optim as Optim


class WarmupOptimizer(object):
    def __init__(self, lr_base, optimizer, data_size, batch_size):
        print('---- init WarmupOptimizer--------')
        self.optimizer = optimizer
        self._step = 0
        self.lr_base = lr_base
        self._rate = 0
        self.data_size = data_size
        self.batch_size = batch_size

    def step(self):
        print('---- call step function ------')
        self._step += 1

        rate = self.rate()
        for p in self.optimizer.param_groups:
            p['lr'] = rate
        self._rate = rate

        self.optimizer.step()

    def zero_grad(self):
        print('---- call zero_grad function -------')
        self.optimizer.zero_grad()

    def rate(self, step=None):
        print('---- call rate function ------------')
        if step is None:
            step = self._step

        if step <= int(self.data_size / self.batch_size * 1):
            r = self.lr_base * 1/4.
        elif step <= int(self.data_size / self.batch_size * 2):
            r = self.lr_base * 2/4.
        elif step <= int(self.data_size / self.batch_size * 3):
            r = self.lr_base * 3/4.
        else:
            r = self.lr_base

        return r


def get_optim(__C, model, data_size, lr_base=None):
    print('---- call get_optim function ---------')
    if lr_base is None:
        lr_base = __C.LR_BASE

    return WarmupOptimizer(
        lr_base,
        Optim.Adam(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=0,
            betas=__C.OPT_BETAS,
            eps=__C.OPT_EPS
        ),
        data_size,
        __C.BATCH_SIZE
    )


def adjust_lr(optim, decay_r):
    print('---- call adjust_lr function ----')
    optim.lr_base *= decay_r

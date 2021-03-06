# -*- coding:utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

"""This is SearchSpace for network."""
from zeus.common import ClassFactory, ClassType
from zeus.modules.module import Module
from .resnet_general import ResNetGeneral
from zeus.modules.operators.ops import Linear, AdaptiveAvgPool2d, View


@ClassFactory.register(ClassType.SEARCH_SPACE)
class ResNet(Module):
    """Create ResNet SearchSpace."""

    def __init__(self, depth=18, init_plane=64, out_plane=None, stage=4, num_class=10, small_input=True,
                 doublechannel=None, downsample=None):
        """Create layers.

        :param num_reps: number of layers
        :type num_reqs: int
        :param items: channel and stride of every layer
        :type items: dict
        :param num_class: number of class
        :type num_class: int
        """
        super(ResNet, self).__init__()
        self.backbone = ResNetGeneral(small_input, init_plane, depth, stage, doublechannel, downsample)
        self.adaptiveAvgPool2d = AdaptiveAvgPool2d(output_size=(1, 1))
        self.view = View()
        out_plane = out_plane or self.backbone.output_channel
        self.head = Linear(in_features=out_plane, out_features=num_class)

# -*- coding:utf-8 -*-

# Copyright (C) 2020. Huawei Technologies Co., Ltd. All rights reserved.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the MIT License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# MIT License for more details.

"""Flops and Parameters Filter."""
import logging
import time
import zeus
from zeus.common import ClassFactory, ClassType
from .filter_terminate_base import FilterTerminateBase


@ClassFactory.register(ClassType.QUOTA)
class LatencyFilter(FilterTerminateBase):
    """Latency Filter class."""

    def __init__(self):
        super(LatencyFilter, self).__init__()
        self.max_latency = self.restrict_config.latency
        if self.max_latency is not None:
            dataset_cls = ClassFactory.get_cls(ClassType.DATASET)
            self.dataset = dataset_cls()
            from zeus.datasets import Adapter
            self.dataloader = Adapter(self.dataset).loader

    def is_filtered(self, desc=None):
        """Filter function of latency."""
        if self.max_latency is None:
            return False
        model, count_input = self.get_model_input(desc)
        num = 100
        if zeus.is_torch_backend():
            start_time = time.time()
            for i in range(num):
                model(count_input)
            latency = (time.time() - start_time) / num
        elif zeus.is_tf_backend():
            import tensorflow as tf
            input = tf.placeholder(tf.float32, shape=count_input.get_shape().as_list())
            output = model(input, training=False)
            with tf.compat.v1.Session() as sess:
                input_numpy = count_input.eval(session=sess)
                start_time = time.time()
                for i in range(num):
                    sess.run(output, feed_dict={input: input_numpy})
                latency = (time.time() - start_time) / num
        logging.info('Sampled model\'s latency: {}'.format(latency))
        if latency > self.max_latency:
            return True
        else:
            return False

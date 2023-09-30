# Copyright The Lightning AI team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Any, ContextManager, Literal

import torch
from lightning_utilities.core.apply_func import apply_to_collection
from torch import Tensor
from torch.nn import Module

from lightning.fabric.plugins.precision.precision import Precision
from lightning.fabric.plugins.precision.utils import (
    _convert_fp_tensor,
    _DtypeContextManager,
)


class HalfPrecision(Precision):
    """Plugin for training with half precision.

    Args:
        precision: Whether to use ``torch.float16`` (``'16-true'``) or ``torch.bfloat16`` (``'bf16-true'``).

    """

    precision: Literal["bf16-true", "16-true"] = "16-true"

    def __init__(self, precision: Literal["bf16-true", "16-true"] = "16-true") -> None:
        self.precision = precision
        self._desired_input_dtype = torch.bfloat16 if precision == "bf16-true" else torch.float16

    def convert_module(self, module: Module) -> Module:
        return module.to(dtype=self._desired_input_dtype)

    def init_context(self) -> ContextManager:
        return _DtypeContextManager(self._desired_input_dtype)

    def forward_context(self) -> ContextManager:
        return _DtypeContextManager(self._desired_input_dtype)

    def convert_input(self, data: Any) -> Any:
        return apply_to_collection(data, function=_convert_fp_tensor, dtype=Tensor, dst_type=self._desired_input_dtype)

    def convert_output(self, data: Any) -> Any:
        return apply_to_collection(data, function=_convert_fp_tensor, dtype=Tensor, dst_type=torch.get_default_dtype())

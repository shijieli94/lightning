import pytest
import torch.nn
from tests_pytorch.helpers.runif import RunIf

import lightning.fabric
from lightning.pytorch import Trainer
from lightning.pytorch.demos.boring_classes import BoringModel
from lightning.pytorch.plugins.precision.double import LightningDoublePrecisionModule
from lightning.pytorch.plugins.precision.fsdp import FSDPMixedPrecisionPlugin
from lightning.pytorch.strategies import DDPStrategy, FSDPStrategy


def test_configure_sharded_model():
    class MyModel(BoringModel):
        def configure_sharded_model(self) -> None:
            ...

    model = MyModel()
    trainer = Trainer(devices=1, accelerator="cpu", fast_dev_run=1)
    with pytest.deprecated_call(match="overridden `MyModel.configure_sharded_model"):
        trainer.fit(model)

    class MyModelBoth(MyModel):
        def configure_model(self):
            ...

    model = MyModelBoth()
    with pytest.raises(
        RuntimeError, match="Both `MyModelBoth.configure_model`, and `MyModelBoth.configure_sharded_model`"
    ):
        trainer.fit(model)


def test_ddp_is_distributed():
    strategy = DDPStrategy()
    with pytest.deprecated_call(match="is deprecated"):
        _ = strategy.is_distributed


@RunIf(min_torch="1.13")
def test_fsdp_activation_checkpointing(monkeypatch):
    with pytest.raises(ValueError, match="cannot set both `activation_checkpointing"):
        FSDPStrategy(activation_checkpointing=torch.nn.Linear, activation_checkpointing_policy=lambda *_: True)

    monkeypatch.setattr(lightning.fabric.strategies.fsdp, "_TORCH_GREATER_EQUAL_2_1", True)
    with pytest.deprecated_call(match=r"use `FSDPStrategy\(activation_checkpointing_policy"):
        FSDPStrategy(activation_checkpointing=torch.nn.Linear)


def test_double_precision_wrapper():
    with pytest.deprecated_call(match=r"The `LightningDoublePrecisionModule` is deprecated and no longer needed"):
        LightningDoublePrecisionModule(BoringModel())


@RunIf(min_torch="1.12")
def test_fsdp_mixed_precision_plugin():
    with pytest.deprecated_call(match=r"The `FSDPMixedPrecisionPlugin` is deprecated"):
        FSDPMixedPrecisionPlugin(precision="16-mixed", device="cuda")

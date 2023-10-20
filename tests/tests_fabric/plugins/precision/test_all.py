import pytest
import torch
from tests_fabric.helpers.runif import RunIf

from lightning.fabric.plugins import (
    DeepSpeedPrecision,
    DoublePrecision,
    FSDPPrecision,
    HalfPrecision,
)


@pytest.mark.parametrize(
    "precision",
    [
        DeepSpeedPrecision("16-true"),
        DoublePrecision(),
        HalfPrecision(),
        pytest.param("fsdp", marks=RunIf(min_torch="1.12")),
    ],
)
def test_default_dtype_is_restored(precision):
    if precision == "fsdp":
        precision = FSDPPrecision("16-true")

    contexts = (
        (precision.init_context, precision.forward_context)
        if not isinstance(precision, DeepSpeedPrecision)
        else (precision.init_context,)
    )
    for context in contexts:
        assert torch.get_default_dtype() is torch.float32
        with pytest.raises(RuntimeError, match="foo"), context():
            assert torch.get_default_dtype() is not torch.float32
            raise RuntimeError("foo")
        assert torch.get_default_dtype() is torch.float32

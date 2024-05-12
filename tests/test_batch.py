import pytest

from app.model import Batch, OrderLine


@pytest.fixture
def order_line() -> OrderLine:
    sku = "SMALL-TABLE"
    return OrderLine(sku, 2)


@pytest.fixture
def batch_reference() -> str:
    return "adsasd21312"


def test_allocate_reduces_qty(batch_reference: str, order_line: OrderLine):
    batch = Batch(batch_reference, order_line.sku, 20)
    batch.allocate(order_line)
    assert batch.qty == 18


def test_allocate_error_if_not_enough_qty(batch_reference: str,
                                          order_line: OrderLine):
    batch = Batch(batch_reference, order_line.sku, 1)
    with pytest.raises(Exception):
        batch.allocate(order_line)


def test_dont_allocate_line_twice(batch_reference: str, order_line: OrderLine):
    batch = Batch(batch_reference, order_line.sku, 10)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.qty == 8

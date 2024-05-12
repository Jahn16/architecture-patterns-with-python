from typing import Callable

import pytest

from app.model import Batch, OrderLine

MakeOrderLine = Callable[[str, int], OrderLine]
MakeBatch = Callable[[str, int], Batch]


@pytest.fixture
def sku() -> str:
    return "SMALL-TABLE"


@pytest.fixture
def make_order_line() -> MakeOrderLine:
    def _make_order_line(sku: str, qty: int) -> OrderLine:
        order_id = "order-id"
        order_line = OrderLine()
        order_line.order_id = order_id
        order_line.sku = sku
        order_line.qty = qty
        return order_line
    return _make_order_line


@pytest.fixture
def make_batch() -> MakeBatch:
    def _make_batch(sku: str, qty: int) -> Batch:
        reference = "test-reference"
        return Batch(reference, sku, qty)
    return _make_batch


def test_allocate_reduces_qty(
        sku: str,
        make_batch: MakeBatch,
        make_order_line: MakeOrderLine) -> None:
    batch = make_batch(sku, 20)
    order_line = make_order_line(sku, 2)
    batch.allocate(order_line)
    assert batch.available_qty == 18


def test_cannot_allocate_if_not_enough_qty(
    sku: str, make_batch: MakeBatch, make_order_line: MakeOrderLine
) -> None:
    batch = make_batch(sku, 10)
    order_line = make_order_line(sku, 15)
    with pytest.raises(Exception):
        batch.allocate(order_line)


def test_can_allocate_equal_qty(sku: str, make_batch: MakeBatch,
                                make_order_line: MakeOrderLine) -> None:
    qty = 10
    batch = make_batch(sku, qty)
    order_line = make_order_line(sku, qty)
    batch.allocate(order_line)
    assert batch.available_qty == 0


def test_cannot_allocate_if_sku_mismatch(
        make_batch: MakeBatch,
        make_order_line: MakeOrderLine) -> None:
    qty = 1
    batch = make_batch("sku", qty)
    order_line = make_order_line("another-sku", qty)
    with pytest.raises(Exception):
        batch.allocate(order_line)


def test_can_only_deallocate_allocated_lines(
        sku: str,
        make_batch: MakeBatch,
        make_order_line: MakeOrderLine) -> None:
    qty = 10
    batch = make_batch(sku, qty)
    order_line = make_order_line(sku, qty)
    with pytest.raises(Exception):
        batch.deallocate(order_line)


def test_cannot_allocate_same_order_twice(
        sku: str,
        make_batch: MakeBatch,
        make_order_line: MakeOrderLine) -> None:
    batch = make_batch(sku, 10)
    order_line = make_order_line(sku, 5)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.available_qty == 5

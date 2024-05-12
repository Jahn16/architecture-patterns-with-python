from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Product:
    sku: str


dataclass(frozen=True)


class OrderLine:
    order_id: str
    sku: str
    qty: int

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OrderLine):
            return False
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)


class Order:
    reference = str
    order_lines = list[OrderLine]


class Batch:
    def __init__(self, reference: str, sku: str, qty: int):
        self.reference = reference
        self.sku = sku
        self._initial_qty = qty
        self.eta = None
        self._allocations: list[OrderLine] = []

    @property
    def allocated_qty(self) -> int:
        return sum(ol.qty for ol in self._allocations)

    @property
    def available_qty(self) -> int:
        return self._initial_qty - self.allocated_qty

    def allocate(self, order_line: OrderLine) -> None:
        if self.available_qty < order_line.qty:
            raise Exception(
                f"Available quantity {self.available_qty} is less than "
                f"order line quantity {order_line.qty}"
            )
        if self.sku != order_line.sku:
            raise Exception(
                f"Batch SKU {self.sku} does not match "
                f"order line SKU {order_line.sku}"
            )
        if order_line in self._allocations:
            return
        self._allocations.append(order_line)

    def deallocate(self, order_line: OrderLine) -> None:
        if order_line not in self._allocations:
            raise Exception(
                f"Order line {order_line.order_id} was not allocated")
        self._allocations.remove(order_line)

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    sku: str


dataclass(frozen=True)


class OrderLine:
    sku: str
    qty: int


class Order:
    reference = str
    order_lines = list[OrderLine]


class Batch:
    def __init__(self, reference: str, sku: str, qty: int):
        self.reference = reference
        self.sku = sku
        self.qty = qty
        self.eta = None

    def allocate(self, order_line: OrderLine) -> None:
        pass

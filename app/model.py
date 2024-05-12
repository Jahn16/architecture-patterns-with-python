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
        self.available_qty = qty
        self.eta = None

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
        self.available_qty -= order_line.qty

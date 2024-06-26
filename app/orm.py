
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import registry

from app.model import OrderLine

mapper_registry = registry()

order_lines = Table("order_lines", mapper_registry.metadata,
                    Column("id", Integer, primary_key=True,
                           autoincrement=True,),
                    Column("sku", String(255)),
                    Column("qty", Integer, nullable=False),
                    Column("orderid", String(255)))


def start_mappers() -> None:
    mapper_registry.map_imperatively(OrderLine, order_lines)

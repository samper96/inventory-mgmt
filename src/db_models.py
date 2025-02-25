"""
Databse models.

This module defines SQLAlchemy ORM models for the Inventory Management System.
"""

from sqlalchemy import Column, Integer, String
from database import Base


class Product(Base):
    """
    Product Model.

    Represents an inventory product with a unique ID, name, and stock quantity.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    stock = Column(Integer, default=0)

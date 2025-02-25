"""
Pydantic Schemas.

Defines request/response schemas used for data validation in the Inventory Management System API.
"""

from pydantic import BaseModel


class ProductBase(BaseModel):
    """Base schema for product attributes."""

    name: str
    stock: int


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    pass


class ProductResponse(ProductBase):
    """Schema for returning a product in API responses."""

    id: int

    class Config:
        orm_mode = True  # Enables ORM compatibility with SQLAlchemy models

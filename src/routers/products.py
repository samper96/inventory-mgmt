"""
Product API Router.

Handles the CRUD operations for products in the Inventory Management System.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from database import get_db
from db_models import Product
from schemas import ProductCreate, ProductResponse
from routers.websocket import connection_manager

router = APIRouter(prefix="/products", tags=["Products"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product in the inventory.

    Args:
        product (ProductCreate): Product data from request body.
        db (Session): Database session object.

    Returns:
        ProductResponse: Created product details.

    Raises:
        HTTPException: 400 if there is a record conflict, 500 for unexpected errors.
    """
    logger.info(f"Attempting to create product: name={product.name}, stock={product.stock}")
    product = Product(name=product.name, stock=product.stock)
    db.add(product)

    try:
        db.commit()
        db.refresh(product)
        logger.info("Product successfully created: ID=%d" % product.id)
        return product
    except IntegrityError:
        db.rollback()
        status_code = 400
        error_detail = "Product creation failed due to integrity constraint."
        logger.warning(error_detail)
        raise HTTPException(status_code=status_code, detail=error_detail)
    except SQLAlchemyError as e:
        db.rollback()
        status_code = 500
        error_detail = "Unexpected database error occurred: %s" % (str(e))
        logger.error(error_detail, exc_info=True)
        raise HTTPException(status_code=status_code, detail=error_detail)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The unique ID of the product.
        db (Session): Database session object.

    Returns:
        ProductResponse: Product details if found, else 404 error.

    Raises:
        HTTPException: 404 if product is not found, 500 for unexpected errors.
    """
    logger.info("Fetching product with ID=%d" % product_id)
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
    except SQLAlchemyError as e:
        status_code = 500
        error_detail = "Unexpected database error occurred: %s" % (str(e))
        logger.error(error_detail, exc_info=True)
        raise HTTPException(status_code=status_code, detail=error_detail)

    if product is None:
        status_code = 400
        error_detail = "Product with ID=%d not found" % product_id
        logger.warning(error_detail)
        raise HTTPException(status_code=status_code, detail=error_detail)

    logger.info("Product fetched: name=%s (ID=%d, stock=%d)" % (product.name, product.id, product.stock))
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_stock(product_id: int, stock: int, db: Session = Depends(get_db)):
    """
    Update the stock for a specific product.
    Broadcasts the stock change via WebSocket to all clients.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        status_code = 404
        error_msg = "Product not found"
        raise HTTPException(status_code=status_code, detail=error_msg)

    product.stock = stock
    db.commit()
    db.refresh(product)

    # Broadcast the update
    message = "Product %d stock updated to %d" % (product_id, stock)
    await connection_manager.broadcast(message)

    return product

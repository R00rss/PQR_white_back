from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from models import products_model
from uuid import UUID

# importar el modelo de producto
from schemas.products import ProductCreate, ProductUpdate, ProductDelete

# PRODUCT CRUD

#  Create product


def create_product(db: Session, product: ProductCreate):
    product_in_db = (
        db.query(products_model.Product)
        .filter(products_model.Product.product_name == product.product_name)
        .first()
    )

    if product_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Product already registered"
        )

    db_product = products_model.Product(
        product_name=product.product_name, is_active=product.is_active
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


# Get product by uuid


def get_product_by_uuid(db: Session, productid: UUID):
    product_in_db = (
        db.query(products_model.Product)
        .options(joinedload(products_model.Product.incidences))
        .filter(products_model.Product.product_id == productid)
        .first()
    )

    if not product_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product_in_db


# Get product by name


def get_product_by_name(db: Session, product_name: str):
    product_in_db = (
        db.query(products_model.Product)
        .options(joinedload(products_model.Product.incidences))
        .filter(products_model.Product.product_name == product_name)
        .first()
    )

    if not product_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product_in_db


# Get all products


def get_all_product(db: Session):
    products_in_db = (
        db.query(products_model.Product)
        .options(joinedload(products_model.Product.incidences))
        .all()
    )

    if not products_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products not found"
        )

    return products_in_db


# UPDATE PRODUCT


def update_product(db: Session, product: ProductUpdate):
    product_in_db = (
        db.query(products_model.Product)
        .options(joinedload(products_model.Product.incidences))
        .filter(products_model.Product.product_id == product.product_id)
        .first()
    )

    if not product_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product_in_db.product_name = product.product_name
    product_in_db.is_active = product.is_active

    db.commit()
    db.refresh(product_in_db)

    return product_in_db


# DELETE PRODUCT


def delete_product(db: Session, product: ProductDelete):
    product_in_db = (
        db.query(products_model.Product)
        .options(joinedload(products_model.Product.incidences))
        .filter(products_model.Product.product_id == product.product_id)
        .first()
    )

    if not product_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    db.delete(product_in_db)
    db.commit()

    return product_in_db

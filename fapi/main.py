
from sqlalchemy.orm import Session
from fapi.database import Base, SessionLocal, get_db, engine
from models import Category, Product
from shem import CategoryBase, ProductBase
from fastapi import Depends, FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.post("/categories/")
def create_category(category: CategoryBase):
    db = SessionLocal()
    db_category = Category(category)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()
    return db_category

@app.post("/product/")
def create_product(product: ProductBase, category_name: str):
    db = SessionLocal()
    db_product = Product(product, category=category_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product

@app.get("/category/kateg")
def read_category( db: Session = Depends(get_db)):
    category = db.query(Category).all()
    return category

@app.get("/product/prod")
def read_product(product: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product).all()
    return product




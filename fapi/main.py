from sqlalchemy.orm import Session
from database import get_db
from models import Category, Product
from shem import CategoryBase, ProductBase
from fastapi import Depends, FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/categories/")
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    db_category = Category(category)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.post("/product/")
def create_product(product: ProductBase, category_name: str, db: Session = Depends(get_db)):
    db_product = Product(product, category=category_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/category/kateg") #получение категорий 
def read_category(db: Session = Depends(get_db)):
    category = db.query(Category).all()
    return category

@app.get("/product/prod") #получение продуктов
def read_product(product: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product).all()
    return product




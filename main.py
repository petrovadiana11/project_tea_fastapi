from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/prtea"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    category = relationship("Category", back_populates="name")
    image = Column(String, index=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

Base.metadata.create_all(bind=engine)

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    price: int
    image: str

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    name: str
    category: CategoryOut

    class Config:
        orm_mode = True


@app.post("/categories/", response_model=CategoryOut)
def create_category(category: CategoryCreate):
    db = SessionLocal()
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    db.close()
    return db_category

@app.post("/product/", response_model=ProductOut)
def create_product(product: ProductCreate, category_name: str):
    db = SessionLocal()
    db_product = Product(**product.dict(), category=category_name)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()
    return db_product

@app.get("/category/{category_id}", response_model=CategoryOut)
def read_category(category_id: int):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == category_id).first()
    db.close()
    if category is None:
        raise HTTPException(status_code=404, detail="User not found")
    return category

@app.get("/product/{product_id}", response_model=ProductOut)
def read_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return product




import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=250), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'
class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=250), nullable=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship("Publisher", backref="books")

    def __str__(self):
        return f'{self.id}: {self.title}, {self.publisher.name}'
class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=250), unique=True)

class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=True)
    count = sq.Column(sq.Integer, nullable=False)
    shop = relationship("Shop", backref="stocks")

    def __str__(self):
        return f'{self.id}: {self.count}, {self.shop.name}'

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=True)
    date_sale = sq.Column(sq.Text, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=True)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship("Stock", backref="sales")

    def __str__(self):
        return f'{self.id}: {self.price}, {self.date_sale}'
def create_tables(engine):
    Base.metadata.create_all(engine)

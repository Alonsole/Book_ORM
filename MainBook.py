import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from BookBase import create_tables, Publisher, Shop, Book, Stock, Sale


class Connectbase:
    def __init__(self, name, passw, server, port, name_db, sqlm, data=None, requestinf=None):
        self.name = name
        self.passw = passw
        self.server = server
        self.port = port
        self.database = name_db
        self.bookdata = data
        self.sqlm = sqlm
        self.requestinf = requestinf
        self.DSN = f"{self.sqlm}://{self.name}:{self.passw}@{self.server}:{self.port}/{self.database}"


    def start(self):
        engine = sqlalchemy.create_engine(self.DSN)
        create_tables(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.close()
        print("Создано")

    def loadjson(self):
        engine = sqlalchemy.create_engine(self.DSN)
        create_tables(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()
        session.close()
        print("Загружено")

    def loadinf(self):
        engine = sqlalchemy.create_engine(self.DSN)
        create_tables(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        if self.requestinf.isdigit():
            find_book = Publisher.id
        else:
            find_book = Publisher.name

        query = (session.query(Book.title,
                              Publisher.name,
                              Sale.price,
                              Sale.date_sale).
                                join(Stock, Stock.id == Sale.id_stock).
                                join(Book, Book.id == Stock.id_book).
                                join(Publisher, Publisher.id == Book.id_publisher))
        result = query.filter(find_book == self.requestinf).all()
        for r in result:
            date = (r.date_sale.split('T')[0]).split('-')
            print(f"{r.title} | {r.name} | {r.price} | {date[2]}-{date[1]}-{date[0]}")
        print('Вывод информации завершён')
        session.close()

with open('fixtures/tests_data.json', 'r') as f:
    data = json.load(f)

if __name__ == "__main__":
    name = "postgres"
    passw = input("Введите пароль базы данных:")
    server = "localhost"
    port = "5432"
    name_db = "bookdb"
    sqlm = "postgresql" #подключается к БД любого типа на ваш выбор

    """создание базы"""
    # Connectbase(name, passw, server, port, name_db, sqlm).start()
    """Залить данные в базу"""
    # Connectbase(name, passw, server, port, name_db, sqlm, data).loadjson()
    """Получить информацию из базы"""
    requestinf = input("Введите имя или идентификатор издателя (publisher): ")
    Connectbase(name, passw, server, port, name_db, sqlm, None, requestinf).loadinf()
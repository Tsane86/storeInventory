import datetime
import csv
import time

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)  # create a session
session = Session()  # create a session instance
Base = declarative_base()  # create a base class

#create the Item table
class Item(Base):  # Table name: item
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)  # primary key is id
    name = Column(String)
    price = Column(Integer)  # must be int
    date = Column(Date) 
    quantity= Column(Integer)

    def __repr__(self):  # return string representation of object
        return "<Item(name='%s', price='%s', date='%s')>" % (
            self.name, self.price, self.date)

#clean data before adding to database
def clean_date(date_str):
    date_str = date_str.split('/')
    month = int(date_str[0])
    day = int(date_str[1])
    year =  int(date_str[2])
    return datetime.date(year, month, day)

def clean_price(price_str):
    return float(price_str.replace('$', '').replace(',', ''))

def convert_float_to_int(num):
    return int(num)

# add all items from csv file to database
def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            if session.query(Item).filter_by(name=row[0]).one_or_none() is None:
                item = Item(name=row[0], price=convert_float_to_int(clean_price(
                    row[1])), quantity=row[2], date=clean_date(row[3]))
                session.add(item)
        session.commit()

# add Item to database
def add_item(name, price, quantity, date):
    if session.query(Item).filter_by(name=name).one_or_none() is None:
        new_item_name = name
        new_item_price = convert_float_to_int(clean_price(price))
        new_item_date = clean_date(date)
        item = Item(name=new_item_name, price=new_item_price, quantity=quantity, date=new_item_date)
        session.add(item)
    else:
        print('\rPlease enter valid data')
        print('For example: Fruitloops, 5, 8, 01/01/2022 (MM-DD-YYYY)')
    session.commit()

# get all items from database
def get_all_items():
    items = session.query(Item).all()
    return items

# get item from database by ID
def get_item_by_id(id):
    id_options = []
    for item in session.query(Item):
        id_options.append(item.id)
    if int(id) in id_options:
        item = session.query(Item).filter_by(id=id).one()
        print('\rID: ' + str(item.id))
        print('\rName: ' + item.name)
        print('\rPrice: $' + str(item.price))
        print('\rQuantity: ' + str(item.quantity))
        print('\rDate: ' + str(item.date))
    else:
        print('\rPlease enter a valid ID')

# backup all items to csv file
def backup_items():
    with open('backup.csv', 'w') as csvfile:
        data = csv.writer(csvfile)
        for item in get_all_items():
            data.writerow([item.name, item.price, item.quantity, item.date])

#show menu
def show_menu():
    print('\n******** Store Inventory App ********')

    while True:
        print('\nPlease select from the following options:')
        print('\rV: Display an item by its Id')
        print('\rA: Add an item to the Store inventory')
        print('\rB: Backup all iventory items to a csv')
        print('\rQ: Quit the App')

        user_input = input('\rPlease select an option: ').upper()
        if user_input in ['V', 'A', 'B', 'Q']:
            if user_input == 'V':
                get_item_by_id(input('\rPlease enter a valid ID of the item: '))
            elif user_input == 'A':
                print('\nPlease enter the details of the new item:')
                print('\rFor example: Fruitloops, 5, 8, 01/01/2022 (MM-DD-YYYY)')
                add_item(input('\rName: '),
                    input('\rPrice: $'),
                    input('\rQuantity: '),
                    input('\rDate: '))
            elif user_input == 'S':
                get_all_items()
            elif user_input == 'B':
                backup_items()
            elif user_input == 'Q':
                print('\rExiting...')
                time.sleep(1.5)
                exit()
        else:
            print('\rPlease select a valid option')
        

# dunder main
if __name__ == '__main__':
    Base.metadata.create_all(engine)  # create table
    add_csv() # adds all of the items to the table
    show_menu()
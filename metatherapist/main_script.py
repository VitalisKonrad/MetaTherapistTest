import requests
# from sqlalchemy import func, distinct
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, JSON, PickleType, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import psycopg2
#import json

#This is unsecure, but for test it good. We can hide this into system variable for production in future.
AIRTABLE_BASE_ID = 'app0FFO6wcLZUPpjc'
AIRTABLE_API_KEY = 'key9Qer1Xfqr6tuL1'
AIRTABLE_TABLE_NAME = 'Psychotherapists'
POSTGRE_USER = 'postgres'
POSTGRE_PASSWORD = 'Guard1994'
POSTGRE_HOST = 'localhost'
# DataBase need to be created manualy
POSTGRE_DB = 'MetaPsychotherapist'

#Configure connection to airtable
endpoint = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
headers = {
    "Authorization": f'Bearer {AIRTABLE_API_KEY}'
}
url = (f'postgresql+psycopg2://{POSTGRE_USER}:{POSTGRE_PASSWORD}@{POSTGRE_HOST}/{POSTGRE_DB}')
engine = create_engine(url, echo=True)

# engine = create_engine(f'postgresql+psycopg2://{POSTGRE_USER}:{POSTGRE_PASSWORD}@{POSTGRE_HOST}/{POSTGRE_DB}', echo = True)
base = declarative_base()

if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()


def get_airtable_data():
    params = ()
    airtable_records = []
    run = True
    while run is True:
        response = requests.get(endpoint, params=params, headers=headers)
        airtable_response = response.json()
        airtable_records += (airtable_response['records'])
        if 'offset' in airtable_response:
            run = True
            params = (('offset', airtable_response['offset']),)
        else:
            run = False
    return airtable_records



class PsychotherapistData(base):
# Information about Psychotherapist

    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(JSON)
    methods = Column(JSON)
    create_time = Column(String)
    airtable_record_id = Column(String)

base.metadata.create_all(engine)

def migrate_data_airtable_postgre():
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    for i in range(0, (len(get_airtable_data()))):
        person = PsychotherapistData(
            name = get_airtable_data()[i]['fields']['Имя'],
            photo = get_airtable_data()[i]['fields']['Фотография'],
            methods = get_airtable_data()[i]['fields']['Методы'],
            create_time = get_airtable_data()[i]['createdTime'],
            airtable_record_id = get_airtable_data()[i]['id'])
        session.add(person)
        print(id)
    session.commit()
    print (session)
# migrate_data_airtable_postgre()

# exists = db.session.query(db.exists().where(PsychotherapistData.airtable_record_id == get_airtable_data()[0]['id'])).scalar()
from sqlalchemy.sql import exists
# print (session.query(exists().where(PsychotherapistData.airtable_record_id == '45terg5yhdthr')).scalar())
# for name, methods, photo in session.query(PsychotherapistData.name, PsychotherapistData.methods, PsychotherapistData.photo).order_by(PsychotherapistData.airtable_record_id):
#     print (name, methods)

# for photo in session.query(PsychotherapistData.photo).order_by(PsychotherapistData.airtable_record_id):
#     print (photo[0][0]['url'])
# # def add_record_to_postgre():
#
# orders = session.query(PsychotherapistData.airtable_record_id).filter_by(airtable_record_id=PsychotherapistData.airtable_record_id).distinct()
# print(orders)


# Я не знаю как удалить дубликаты с помощью алхимии, поэтому создаю обычное подключение к postgresql
connection =psycopg2.connect(user=POSTGRE_USER,
                             password=POSTGRE_PASSWORD,
                             host=POSTGRE_HOST,
                             port='5432',
                             database=POSTGRE_DB)
def delete_duplicates():
    cursor = connection.cursor()
    cursor.execute("DELETE FROM doctors WHERE ctid NOT IN (SELECT max(ctid) FROM doctors GROUP BY airtable_record_id);")
    connection.commit()
    cursor.close()
# test = get_airtable_data()[0]['fields']['Методы']
# print(test)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
delete_duplicates()
rows_count = session.query(func.count(PsychotherapistData.id)).scalar()

print (rows_count)
for ids in session.query(PsychotherapistData.id).order_by(PsychotherapistData.id):
    ids = ids
    print (ids)
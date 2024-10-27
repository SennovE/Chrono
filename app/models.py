from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
metadata = MetaData()
users = Table('users',metadata,
             Column('id', Integer, primary_key=True),
              Column('name', String, nullable=False),
              Column('password', String, nullable=False) )

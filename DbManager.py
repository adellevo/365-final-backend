from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///local.db', echo = True)
meta = MetaData()

users = Table(
   'users', meta, 
   Column('userId', Integer, primary_key = True), 
   Column('username', String), 
   Column('primary_wallet', String), #or password?
)

wallets = Table(
   'wallets', meta, 
   Column('address', Integer, primary_key = True),
   Column('provider',String)
   Column('userId', String), 
)

Transactions = Table(
   'Transactions', meta, 
   Column('function', string),
   Column('module',String),
   Column('userId',String)
   Column('payloadId', String),
   Column('resultId', String),
   Column('stashId', String), 
)
meta.create_all(engine)

class DbManager:

    def __init__(config):
        self.engine = create_engine('sqlite:///college.db', echo = True)
        self.meta = MetaData()

    def create_user(username,walle):
        return

    def create_stash(userId,txnIds):
        return

    
    def delete_stash(userId,stashId):
        return


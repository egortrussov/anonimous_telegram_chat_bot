import sqlalchemy 
from sqlalchemy import orm 
import sqlalchemy.ext.declarative as dec 

SqlAlchemyBase = dec.declarative_base()

__factory = None

def global_init_db(db_file):
    """
    Initialises and connects to sqlite database 
    :return: None
    """
    global __factory 

    if __factory:
        return 
    
    conn_str = f'sqlite:///{ db_file.strip() }?check_same_thread=False'
    print('Connecting to', conn_str)
    
    engine = sqlalchemy.create_engine(conn_str)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine) 


def create_session() -> orm.Session: 
    """
    Creates orm session 
    :return: sqlalchemy.orm.Session
    """
    global __factory
    return __factory()
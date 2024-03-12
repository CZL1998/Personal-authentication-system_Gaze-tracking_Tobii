from sqlalchemy import create_engine, and_, or_
from src.db.models import *
from sqlalchemy.orm import sessionmaker, scoped_session
import config

class MysqlOrm:
    # engine = create_engine( "{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}?charset={
    # charset}".format(SQLALCHEMY_MYSQL_ENGINE_CONFIG), **SQLALCHEMY_MYSQL_POOL_CONFIG)
    # engine = create_engine(
    #     "{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
    #         **SQLALCHEMY_MYSQL_ENGINE_CONFIG))
    engine = create_engine(f"sqlite:///{config.DATABASE_PATH}", connect_args={"check_same_thread": False})

    def __init__(self):
        self.session = self.make_session()()

    def make_session(self):
        # Scoped_session is a single instance, aim to realize the thread safety Meanwhile, scoped_session realizes
        # the agent mode, able to forward the operations into the object been agent.
        return scoped_session(session_factory=sessionmaker(bind=self.engine))

    def create_all_schemas(self):
        # Base = declarative_base()
        Base.metadata.create_all(self.engine)

    def drop_all_schemas(self):
        Base.metadata.drop_all(self.engine)

    def add(self, instance):
        self.session.add(instance)
        self.session.commit()


if __name__ == '__main__':
    mo = MysqlOrm()
    mo.drop_all_schemas()
    mo.create_all_schemas()
    for gaze in config.GAZES:
        mo.add(Gaze(name=gaze['name'], url=gaze['url']))
    for user in config.USERS:
        mo.add(User(**user))
    result = mo.session.query(Gaze).filter(Gaze.name == 'rd').first()
    if result:
        print(result.__dict__)
    user = mo.session.query(User).filter(
            and_(User.username == 'getty', User.password == '12345', User.gid == 1) 
        ).first()
    if user:
        print(user.__dict__)
    print([user.__dict__ for user in mo.session.query(User).all()])
    print([gaze.__dict__ for gaze in mo.session.query(Gaze).all()])
    # gaze = mo.session.query(User).filter(User.username=='user1').first()
    # print(gaze)
    # print(gaze.__dict__)
    
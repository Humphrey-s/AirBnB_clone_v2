#!/usr/bin/python3
'''database storage engine'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv


user = getenv('HBNB_MYSQL_USER')
password = getenv('HBNB_MYSQL_PWD')
host = getenv("HBNB_MYSQL_HOST")
database = getenv("HBNB_MYSQL_DB")

classes = {"user": User, "city": City, "place": Place, "review": Review, "state": State, "amenities": Amenity}

class DBStorage:

    __engine = None
    __session = None

    def __init__(self):

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(user, password, host, database), pool_pre_ping=True)

        if getenv('HBNB_ENV') == "test":
            self.__session.drop_all(self.__engine)

    def all(self, cls=None):

        dic_t = {}

        for classs in classes.keys():
            if cls is None or cls is classes[classs]:
                objs = self.__session.query(classes[classs]).all()

                for obj in objs:
                    dic_t[obj.__class__.__name__ + "." + obj.id] = obj

        return dic_t

    def new(self, obj):
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e
    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()
    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        self.__session.remove()
        self.__session.close()

#!/usr/bin/python3
"""New engine DBStorage"""
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv


classes = {"City": City, "State": State}


class DBStorage:
    """DB storage Engine"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = "localhost"
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        dbString = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'

        self.__engine = create_engine(dbString, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj

        return (new_dict)

    def new(self, obj):
        """add object to current db session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an object from current db"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in the database
        create the current database session from the session
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """close and save current session to database"""
        self.__session.remove()

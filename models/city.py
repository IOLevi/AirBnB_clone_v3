#!/usr/bin/python3
'''
    Define the class City.
'''
from os import getenv
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.state import State


class City(BaseModel, Base):
    '''
        Define the class City that inherits from BaseModel.
    '''
    __tablename__ = "cities"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete, delete-orphan")
    else:
        state_id = ""
        name = ""
        @property
        def places(self):
            '''
                Return list of city instances if City.state_id==current
                State.id
                FileStorage relationship between State and City
            '''
            list_places = []
            for place in models.storage.all("Place").values():
                if place.city_id == self.id:
                    list_places.append(place)
            return list_places

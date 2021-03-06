# provides a lots of functions which lets connect with the cmd
import sys


from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80) ,nullable = False)
    id = Column(Integer , primary_key = True)

class Menu(Base):
    __tablename__ = 'menu_item'
    name = Column(String(120) , nullable = False)
    id = Column(Integer , primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer , ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        #returns an object in easily serializable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course
        }
        pass

### insert at the end of the



engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

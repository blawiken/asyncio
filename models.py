from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Integer, Column, String


PG_DSN = 'postgresql+asyncpg://postgres:1234@127.0.0.1:5431/netology_asyncio'
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class SwapiPeople(Base):

    __tablename__ = 'swapi_people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(String)
    gender = Column(String)

    mass = Column(String)
    height = Column(String)
    eye_color = Column(String)
    hair_color = Column(String)
    skin_color = Column(String)
    homeworld = Column(String)
    species = Column(String)

    starships = Column(String)
    vehicles = Column(String)

    films = Column(String)

    def __str__(self):
        return self.name
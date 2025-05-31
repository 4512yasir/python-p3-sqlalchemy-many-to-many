from sqlalchemy import ForeignKey, Column, Integer, String, Table, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Naming convention for constraints
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

# Association table for User <-> Game (many-to-many)
user_game_table = Table(
    'user_games',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())

    # Relationships
    reviews = relationship('Review', backref=backref('game'))
    users = relationship('User', secondary=user_game_table, back_populates='games')

    def __repr__(self):
        return f"<Game(id={self.id}, title={self.title}, platform={self.platform})>"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reviews = relationship('Review', backref=backref('user'))
    games = relationship('Game', secondary=user_game_table, back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())
    game_id = Column(Integer(), ForeignKey('games.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))

    def __repr__(self):
        return f"<Review(id={self.id}, score={self.score}, game_id={self.game_id}, user_id={self.user_id})>"

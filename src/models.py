from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates = "user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(80), nullable = False)
    species: Mapped[str] = mapped_column(String(80), nullable = False)
    gender: Mapped[str] = mapped_column(String(80), nullable = False)
    homeworld: Mapped[str] = mapped_column(String(80), nullable = False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates = "people", cascade = "all, delete")

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "gender": self.gender,
            "homeworld": self.homeworld
        }

class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(80), nullable = False)
    climate: Mapped[str] = mapped_column(String(80), nullable = False)
    population: Mapped[str] = mapped_column(String(80), nullable = False)
    terrain: Mapped[str] = mapped_column(String(80), nullable = False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates = "planet", cascade = "all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,

        }
    
class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable = True)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable = True)

    user: Mapped["User"] = relationship("User", back_populates = "favorites")
    planet: Mapped["Planet"] = relationship ("Planet", back_populates = "favorites")
    people: Mapped ["People"] = relationship("People", back_populates = "favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }



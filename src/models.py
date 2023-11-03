from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        # Example below
        return '<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    population = db.Column(db.Integer, nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    diameter = db.Column(db.Float, nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "surface_water": self.surface_water,
            "orbital_period": self.orbital_period
        }

class Character(db.Model):
    __tablename__ = 'character'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    height = db.Column(db.Integer, nullable=True)
    hair_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        # Example below
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    model = db.Column(db.String(250), nullable=True)
    manufacturer = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        # Example below
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "price": self.price
        }
   
class Favorites(db.Model):
    __tablename__ = 'favorites'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(Character)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle = db.relationship(Vehicle)


    def __repr__(self):
        # Example below
        # return '<User %r>' % self.username
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
            # do not serialize the password, its a security breach
        }
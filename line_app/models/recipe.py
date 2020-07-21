from datetime import datetime

from line_app import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_index = db.Column(db.Integer, index=True, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    image_url = db.Column(db.String(255), nullable=False, unique=True)
    recipe_url = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, recipe_index, name, image_url, recipe_url):
        self.recipe_index = recipe_index
        self.name = name
        self.image_url = image_url
        self.recipe_url = recipe_url

    def to_dict(self):
        return {
            'id': self.id,
            'recipe_index': self.recipe_index,
            'name': self.name,
            'image_url': self.image_url,
            'recipe_url': self.recipe_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def commit_db(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_by_recipe_indexes(cls, recipe_indexes):
        recipes = db.session.query(Recipe).filter(Recipe.recipe_index.in_(recipe_indexes)).all()
        return recipes

    @classmethod
    def delete_recipes(cls):
        db.session.query(Recipe).delete()
        return
    
    @classmethod
    def get_all_recipes(cls):
        recipes = db.session.query(Recipe).all()
        return recipes
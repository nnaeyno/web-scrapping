from pymongo import MongoClient

from objects import Ingredient, Step, Recipe


class RecipeRepository:
    def __init__(self, db):
        self.collection = db['recipes']

    def add_recipe(self, recipe: Recipe):
        self.collection.insert_one(recipe.to_dict())

    def get_recipe(self, name: str) -> Recipe:
        data = self.collection.find_one({"name": name})
        if not data:
            return None
        return self._convert_from_dict(data)

    def _convert_from_dict(self, data: dict) -> Recipe:
        ingredients = [Ingredient(**ingredient) for ingredient in data['ingredients']]
        steps = [Step(**step) for step in data['steps']]
        return Recipe(data['name'], ingredients, steps)

    def update_recipe(self, name: str, updated_recipe: Recipe):
        self.collection.update_one({"name": name}, {"$set": updated_recipe.to_dict()})

    def delete_recipe(self, name: str):
        self.collection.delete_one({"name": name})

    def list_all_recipes(self):
        return self.collection.find()


class RecipeService:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    def create_recipe(self, name: str, ingredients: list[Ingredient], steps: list[Step]):
        recipe = Recipe(name, ingredients, steps)
        self.repository.add_recipe(recipe)

    def get_recipe_by_name(self, name: str) -> Recipe:
        return self.repository.get_recipe(name)

    def update_recipe(self, name: str, ingredients: list[Ingredient], steps: list[Step]):
        recipe = Recipe(name, ingredients, steps)
        self.repository.update_recipe(name, recipe)

    def delete_recipe(self, name: str):
        self.repository.delete_recipe(name)

    def list_all_recipes(self):
        return self.repository.list_all_recipes()

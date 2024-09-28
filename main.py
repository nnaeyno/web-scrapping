from database import RecipeRepository, RecipeService
from objects import Ingredient, Step
from scrapping import BS4Scrapping

from pymongo import MongoClient


def create_mongo_client(db_name="recipe_db"):
    client = MongoClient("mongodb://localhost:27017/")
    return client[db_name]


if __name__ == '__main__':
    scrapper = BS4Scrapping()
    scrapper.scrape_recipes()

    # TEST MONGO
    # if __name__ == "__main__":
    #     # Setup MongoDB and repository
    #     db = create_mongo_client()
    #     repository = RecipeRepository(db)
    #     service = RecipeService(repository)
    #
    #     # Example usage
    #     ingredient_list = [Ingredient("Flour", "2 cups"), Ingredient("Sugar", "1 cup")]
    #     step_list = [Step(1, "Mix all ingredients"), Step(2, "Bake for 30 minutes at 180°C")]
    #
    #     # Adding a recipe
    #     service.create_recipe("Cake", ingredient_list, step_list)
    #
    #     # Fetching and displaying a recipe
    #     recipe = service.get_recipe_by_name("Cake")
    #     print(recipe.name)
    #     print("Ingredients:")
    #     for ingredient in recipe.ingredients:
    #         print(f"{ingredient.name} - {ingredient.quantity}")
    #
    #     print("Steps:")
    #     for step in recipe.steps:
    #         print(f"Step {step.step_number}: {step.description}")

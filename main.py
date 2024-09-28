from database import RecipeRepository, RecipeService
from objects import Step
from scrapping import BS4Scrapping

from pymongo import MongoClient

CLEAR = False
def create_mongo_client(db_name="recipe_db"):
    client = MongoClient("mongodb://localhost:27017/")
    return client[db_name]


if __name__ == '__main__':
    scrapper = BS4Scrapping()
    recipes = scrapper.scrape_recipes()

    db = create_mongo_client()
    repository = RecipeRepository(db)
    service = RecipeService(repository)
    if CLEAR:
        service.clear()

    for recipe in recipes:
        if recipe:
            service.create_recipe(recipe)

    avg_steps = service.get_avg_steps()
    most_portions = service.get_most_portions()
    author_with_most_recipes = service.get_author_with_most_recipes()
    avg_ingredients = service.get_avg_ingredients()

    print(f"average steps: {avg_steps}")
    print(f"recipe with most portions: {most_portions}")
    print(f"author with most recipes: {author_with_most_recipes}")
    print(f"average ingredients: {avg_ingredients}")

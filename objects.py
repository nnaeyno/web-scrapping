class Ingredient:
    def __init__(self, name: str, quantity: str):
        self.name = name
        self.quantity = quantity

    def to_dict(self):
        return {
            "name": self.name,
            "quantity": self.quantity
        }

class Step:
    def __init__(self, step_number: int, description: str):
        self.step_number = step_number
        self.description = description

    def to_dict(self):
        return {
            "step_number": self.step_number,
            "description": self.description
        }

class Recipe:
    def __init__(self, name: str, ingredients: list[Ingredient], steps: list[Step]):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps

    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients],
            "steps": [step.to_dict() for step in self.steps]
        }

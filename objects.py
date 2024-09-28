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
    """         რეცეპტის დასახელება
                რეცეპტის მისამართი (URL თვითონ რეცეპტის)
                რეცეპტის მთავარი კატეგორიის დასახელება და მისამართი(URL)
                რეცეპტის ქვეკატეგორიiს დასახელება და მისამართი(URL)
                მთავარი სურათის მისამართი
                მოკლე აღწერა( გარედან რეცეპტს რაც აქვს - რეცეპტის დეტალურიდანაც შეიძლება მაგ ინფოს აღება)
                ავტორი სახელი
                ულუფების რაოდენობა
                რეცეპტის ინგრედიენტები
                რეცეპტის მომზადების ეტაპები"""
    def __init__(self, name: str, ingredients: list[Ingredient], steps: list[Step], category: str, subcategory: str,
                 image_url: str, description: str, author_name: str, portions: int):
        self.name = name
        self.ingredients = ingredients
        self.steps = steps
        self.author_name = author_name
        self.subcategory = subcategory
        self.description = description
        self.image_url = image_url
        self.category = category
        self.subcategory = subcategory
        self.portions = portions


    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": [ingredient.to_dict() for ingredient in self.ingredients],
            "steps": [step.to_dict() for step in self.steps]
        }

import html
import json

import requests
from bs4 import BeautifulSoup
import os

from objects import Recipe, Category


class BS4Scrapping:

    def __init__(self, url: str = "https://kulinaria.ge/"):
        self.base_url = url

    def get_soup(self, url):
        """Fetches a webpage and returns a BeautifulSoup object."""
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def scrape_recipes(self):
        recipes = []
        # Step 1: Load the main page to find the "/receptebi/" link
        main_page_url = f"{self.base_url}/"
        main_soup = self.get_soup(main_page_url)

        # Find the link for "/receptebi/"
        receptebi_link = main_soup.find(
            'a', class_='nav__item recipe-nav-text', href="/receptebi/")['href']
        print(receptebi_link)
        # Step 2: Follow the "/receptebi/" link
        receptebi_url = self.base_url + receptebi_link
        receptebi_soup = self.get_soup(receptebi_url)
        # Step 3: Find the link for "/wvnianebi/"
        recipe_nav_body = receptebi_soup.find('div', class_='recipe__nav-body')

        # We will look for the specific link for "წვნიანები" (wvnianebi)
        wvnianebi_link = recipe_nav_body.find(
            'a', href="/receptebi/cat/wvnianebi/")['href']
        print(wvnianebi_link)
        # Step 4: Follow the "/wvnianebi/" link
        wvnianebi_url = self.base_url + wvnianebi_link
        wvnianebi_soup = self.get_soup(wvnianebi_url)

        # You can now scrape the content of the "/wvnianebi/" page as needed
        # For example, let's print all recipe titles available on this page

        recipe_nav_body = wvnianebi_soup.find('div', class_='recipe__nav-body')

        recipes_list = wvnianebi_soup.find(
            'div', class_='kulinaria-row box-container')
        # recipes_list = recipes_list.find('div', class_='box box--author kulinaria-col-3 box--massonry')
        box_imgs = recipes_list.find_all('div', class_='box__img')

        # Iterate through each "box__img" div and find the href in the <a> tag
        for box_img in box_imgs:
            # Find the <a> tag with an href attribute
            a_tag = box_img.find('a', href=True)
            if a_tag:
                href = a_tag['href']  # Extract the href attribute
                recipes.append(self.scrap_one_recipe(href))
                # print(f"Found URL: {href}")

        return recipes

    def scrap_one_recipe(self, one_recipe_url):
        one_recipe = self.get_soup(self.base_url + one_recipe_url)
        """ რეცეპტის დასახელება
            რეცეპტის მისამართი (URL თვითონ რეცეპტის) - one_recipe_url
            რეცეპტის მთავარი კატეგორიის დასახელება და მისამართი(URL) 
                ( მაგ: {title: სალათები, url: https://kulinaria.ge/receptebi/cat/salaTebi/}) - outer scope
            რეცეპტის ქვეკატეგორიiს დასახელება და მისამართი(URL) 
                ( მაგ: {title: ცხელი სალათები, url: https://kulinaria.ge/receptebi/cat/salaTebi/cxeli-salaTebi/}) - outer scope
            მთავარი სურათის მისამართი 
            მოკლე აღწერა( გარედან რეცეპტს რაც აქვს - რეცეპტის დეტალურიდანაც შეიძლება მაგ ინფოს აღება)
            ავტორი სახელი
            ულუფების რაოდენობა
            რეცეპტის ინგრედიენტები (სიის სახით უნდა შევინახოთ ყველა)
            რეცეპტის მომზადების ეტაპები (თავისი ეტაპის ნომრით და აღწერით) """
        script = one_recipe.find('script', {'type': 'application/ld+json'})
        data = {}

        if script is not None:
            try:
                # Convert HTML entities to their corresponding characters
                unescaped_string = html.unescape(script.string)

                # Parse the JSON from the unescaped script string
                data = json.loads(unescaped_string)
            except json.JSONDecodeError:
                print(f'Error decoding JSON for script: {script.string}')
                return
        else:
            print('No script tag found')
            return

        # Access the data in the JSON
        name = data['name']
        author = data['author']
        description = data['description']
        image = data['image']
        ingredients = data['recipeIngredient']

        instructions = data['recipeInstructions'].split('\n')
        yield_amount = data['recipeYield']

        pagination_items = one_recipe.find_all(
            'a', {'class': 'pagination__item'})
        categories = [
            item for item in pagination_items if "/cat/" in item['href']]
        category, subcategory = None, None
        if len(categories) >= 2:
            category_item = categories[0]
            category = Category(category_item.text, category_item['href'])
            subcategory_item = categories[1]
            subcategory = Category(subcategory_item.text,
                                   subcategory_item['href'])

        recipe = Recipe(name, ingredients,
                        instructions, category, subcategory, image, description, author, yield_amount)
        # print(recipe.to_dict())
        return recipe

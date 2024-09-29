import requests
from bs4 import BeautifulSoup

from objects import Recipe, Category, Step


def get_ingredients(one_recipe):
    ingredients = one_recipe.find_all('div', class_='list__item')

    def parse_one_ingredient(ingredient):
        text = ingredient.get_text(separator=" ", strip=True)
        cleaned_text = ' '.join(text.split())
        return cleaned_text

    ingredients = list(map(parse_one_ingredient, ingredients))
    return ingredients


class BS4Scrapping:

    def __init__(self, url: str = "https://kulinaria.ge"):
        self.base_url = url

    def get_soup(self, url):
        """Fetches a webpage and returns a BeautifulSoup object."""
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def scrape_recipes(self, category_name="wvnianebi"):
        main_page_url = f"{self.base_url}/"
        main_soup = self.get_soup(main_page_url)
        receptebi_link = main_soup.find(
            'a', class_='nav__item recipe-nav-text', href="/receptebi/")['href']
        receptebi_url = self.base_url + receptebi_link
        receptebi_soup = self.get_soup(receptebi_url)
        recipe_nav_body = receptebi_soup.find('div', class_='recipe__nav-body')

        # We will look for the specific link for "წვნიანები" (wvnianebi)
        category_link = recipe_nav_body.find(
            'a', href=f"/receptebi/cat/{category_name}/")['href']

        category_url = self.base_url + category_link
        wvnianebi_soup = self.get_soup(category_url)
        category = Category(wvnianebi_soup.find(
            'h1', class_='title mainLeftSpace').text, category_url)
        sub_categories = wvnianebi_soup.find(
            'div', class_='recipe__nav--view').find('div', class_='recipe__nav-body')
        sub_categories_names = sub_categories.find_all('div', class_='txt')
        sub_categories_urls = hrefs = [a['href']
                                       for a in sub_categories.find_all('a', href=True)]
        recipes = self.scrap_sub_categories(
            sub_categories_urls, sub_categories_names, category)

        return recipes

    def scrap_one_recipe(self, one_recipe_url, category, subcategory):
        one_recipe = self.get_soup(self.base_url + one_recipe_url)
        """ რეცეპტის დასახელება
            რეცეპტის მისამართი (URL თვითონ რეცეპტის) - one_recipe_url
            რეცეპტის მთავარი კატეგორიის დასახელება და მისამართი(URL) 
                ( მაგ: {title: სალათები, url: https://kulinaria.ge/receptebi/cat/salaTebi/}) - outer scope
            რეცეპტის ქვეკატეგორის დასახელება და მისამართი(URL) 
                ( მაგ: {title: ცხელი სალათები, url: https://kulinaria.ge/receptebi/cat/salaTebi/cxeli-salaTebi/}) - outer scope
            მთავარი სურათის მისამართი 
            მოკლე აღწერა( გარედან რეცეპტს რაც აქვს - რეცეპტის დეტალურიდანაც შეიძლება მაგ ინფოს აღება)
            ავტორი სახელი
            ულუფების რაოდენობა
            რეცეპტის ინგრედიენტები (სიის სახით უნდა შევინახოთ ყველა)
            რეცეპტის მომზადების ეტაპები (თავისი ეტაპის ნომრით და აღწერით) """

        name = one_recipe.find('div', class_='post__title').find('h1').text
        ingredients = get_ingredients(one_recipe)
        image = self.base_url + \
            one_recipe.find('div', class_='post__img').find('img')["src"]
        description = one_recipe.find(
            'div', class_='post__description').text.strip()
        author = one_recipe.find(
            'div', class_='post__author').find('a').text.strip()
        portion = self.get_portion(one_recipe)
        instructions = self.get_instructions(one_recipe)
        recipe = Recipe(name, ingredients,
                        instructions, category, subcategory, image, description, author, portion)
        return recipe

    def get_portion(self, one_recipe):
        portion = one_recipe.findAll('div', class_='lineDesc__item')[
            1].text.strip()
        portion = portion.split()
        return int(portion[0]) if len(portion) > 1 else 1

    def get_instructions(self, one_recipe):
        instructions = one_recipe.findAll('div', class_='lineList__item')
        instructions = list(
            map(lambda x: x.find('p').text.strip(), instructions))
        result = []
        for step_number, step_desc in enumerate(instructions):
            step = Step(step_number, step_desc)
            result.append(step)
        return result

    def scrap_sub_categories(self, sub_categories_urls, sub_categories_names, category_name):
        all_recipes = []
        for ind, sub_category_url in enumerate(sub_categories_urls):
            sub_category = Category(
                sub_categories_names[ind].text, self.base_url + sub_category_url)
            all_recipes += (self.scrap_one_sub_category(sub_category, category_name))
        return all_recipes

    def scrap_one_sub_category(self, sub_category, category_name):
        soup = self.get_soup(sub_category.url)
        recipes = []
        recipes_list = soup.find(
            'div', class_='kulinaria-row box-container')
        box_imgs = recipes_list.find_all('div', class_='box__img')

        # Iterate through each "box__img" div and find the href in the <a> tag
        for box_img in box_imgs:
            # Find the <a> tag with an href attribute
            a_tag = box_img.find('a', href=True)
            if a_tag:
                href = a_tag['href']  # Extract the href attribute
                recipes.append(self.scrap_one_recipe(
                    href, category_name, sub_category))

        return recipes

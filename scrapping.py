import requests
from bs4 import BeautifulSoup
import os


class BS4Scrapping():

    def __init__(self, url: str = "https://kulinaria.ge/"):
        self.base_url = url

    def get_soup(self, url):
        """Fetches a webpage and returns a BeautifulSoup object."""
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def scrape_receptebi(self):
        # Step 1: Load the main page to find the "/receptebi/" link
        main_page_url = f"{self.base_url}/"
        main_soup = self.get_soup(main_page_url)

        # Find the link for "/receptebi/"
        receptebi_link = main_soup.find('a', class_='nav__item recipe-nav-text', href="/receptebi/")['href']
        print(receptebi_link)
        # Step 2: Follow the "/receptebi/" link
        receptebi_url = self.base_url + receptebi_link
        receptebi_soup = self.get_soup(receptebi_url)
        # Step 3: Find the link for "/wvnianebi/"
        recipe_nav_body = receptebi_soup.find('div', class_='recipe__nav-body')

        # We will look for the specific link for "წვნიანები" (wvnianebi)
        wvnianebi_link = recipe_nav_body.find('a', href="/receptebi/cat/wvnianebi/")['href']
        print(wvnianebi_link)
        # Step 4: Follow the "/wvnianebi/" link
        wvnianebi_url = self.base_url + wvnianebi_link
        wvnianebi_soup = self.get_soup(wvnianebi_url)

        # You can now scrape the content of the "/wvnianebi/" page as needed
        # For example, let's print all recipe titles available on this page

        recipe_nav_body = wvnianebi_soup.find('div', class_='recipe__nav-body')

        recipes_list = wvnianebi_soup.find('div', class_='r')
        # Find all divs with class "txt" inside the "recipe__nav-body"
        recipe_titles = recipe_nav_body.find_all('div', class_='txt')
        # recipe_titles = wvnianebi_soup.find_all('div', class_='recipe__title')  # Hypothetical class for recipe titles
        for title in recipe_titles:
            print(title.text.strip())

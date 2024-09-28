
# Recipe Scraper App
This application scrapes recipes from the kulinaria.ge website using Beautiful Soup and stores the scraped data in a MongoDB database.<br> 
It extracts information such as the recipe name, ingredients, steps, category, subcategory, portions, and other metadata, saving them  <br> 
for later retrieval or use in other applications.

## Features
* Scrapes recipe data from the kulinaria.ge website.
* Extracts:
  * Recipe name
  * Ingredients
  * Steps (with detailed instructions)
  * Category (main category and subcategory)
  * Portions (servings)
  * Description
  * Author name
  * Image URL
* Stores the extracted data in a MongoDB database for easy access and querying.
## Technologies Used
* Python for the core logic and scraping.
* Beautiful Soup for parsing the HTML and scraping data from the website.
* Requests for making HTTP requests to fetch web pages.
* MongoDB for storing the scraped recipe data.
* pymongo to interact with the MongoDB database.
## Requirements
To run this application, make sure you have the following dependencies installed:
* Python 3.11
* BeautifulSoup4
* Requests
* pymongo
* MongoDB server (ensure MongoDB is running on localhost:27017 or update the connection string in the code)
* Python Dependencies
* Install Python dependencies using pip:
## Setup
1. Install the required Python libraries with pip:
`pip install requirements.txt`
2. Ensure you have a running MongoDB instance. The script will connect to MongoDB at `mongodb://localhost:27017/` by default.
## Usage
Run the main script with Python:
```python main.py```
This will scrape recipes from the website, store them in the MongoDB database, and print out some basic analysis of the collected recipes:
- Average number of steps per recipe
- Recipe with the most portions
- Author with the most recipes
- Average number of ingredients per recipe
## Code Overview
The main script imports several modules:
- `database`: Contains `RecipeRepository` and `RecipeService` classes for interacting with the MongoDB database.
- `objects`: Contains the classes `Step`, `Ingredient`, `Recipe` that represent the database objects.
- `scrapping`: Contains the BS4Scrapping class for scraping recipes from the website.
The script first creates an instance of BS4Scrapping and uses it to scrape recipes from the website. It then creates a MongoDB client and a RecipeRepository for the database. The RecipeService is used to interact with the repository.
For each scraped recipe, the script uses the service to store the recipe in the database. It then uses the service to perform the analysis and print out the results.
## Troubleshooting
If you encounter issues while running the scraper:

1. MongoDB Connection Issues:

   * Make sure MongoDB is running on localhost:27017. 
   * If MongoDB is hosted on another server or port, update the connection string accordingly.
2. Beautiful Soup Parsing Errors:
   * Ensure the HTML structure of the website hasn't changed. If so, you may need to update the scraping logic in scraper.py to reflect the new structure.

## Author
Developed by Lizi Ekseulidze, Nino Gogoberishvili.
# Recipe Scraper and Analyzer
This project scrapes recipes from a website, stores them in a MongoDB database, and performs some basic analysis on the collected data.
## Dependencies
This project uses the following Python libraries:
- pymongo for interacting with MongoDB
- requests and beautifulsoup4 for web scraping
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

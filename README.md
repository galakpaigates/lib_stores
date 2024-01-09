# LIB STORES
#### Video Demo:  https://youtu.be/1aMh_R8f21k
#### Description:

### This project is main aimed at Stores and Customers. It makes it possible for local Liberian Stores / Businesses to upload their products on the site. When the Store uploads their products to the site, Customers can visit the site and view the different products that are available in the store.
### Customers also have the ability to purchase products and a request message will be sent to the store containing information about how many product that particular product wants.
### This project also makes it possible for customers to pay with their Local Currency(LRD) or United States Dollars. It also uses a common money transfers means called, Mobile Money which is very common in Liberia, unlike Bank accounts and credit cards.

### LIB Stores also solves a major problem in finding the particular product you wish to buy. Instead of transporting yourself from store to store, asking for the product you wish to purchase, a customer could just check on the site and search the stores for the product they want to purchase. In this way, the customer has a very good place to begin whenever they have a product they need to find and buy.

### There are other functionalities and features that will be added to the project as time goes by, but that's that for now.


## Implementation Details:
### app.py - Where I import and run my flask application
### lib_stores.db - My sqlite3 relational file database I use to store information
### queries.sql - Used to store the queries I used to create various tables in my database
### website/ (folder) - used to store my templates and static directories (just my custom project structure)
### __init__.py - used to initialize and configure my flask application then return the app to be run in app.py
### routes.py - used to create a blueprint that has all of my routes or views in it and some validations
### utils.py - used to store helper functions and other constants that I may need in multiple files
### templates/ (folder) - used to store my html templates to render for specific routes
### static/ (folder) - used to store static files that won't ever change, like images, css and js files and a place to temporarily store uploaded images to be read into the database
### README.md - is what you're currently going through and it summarizes my project

#### Project Idea Credit:
## Jee-hyea Grace Arkoi

## I'm galakpaigates
## This was CS50.

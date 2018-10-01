# Fast-Food-Fast-DB
This is a food delivery service application for a restaurant using a Database 

[![Build Status](https://travis-ci.org/celestemiriams/Fast-Food-Fast-DB.svg?branch=develop)](https://travis-ci.org/celestemiriams/Fast-Food-Fast-DB)

[![Coverage Status](https://coveralls.io/repos/github/celestemiriams/Fast-Food-Fast-DB/badge.svg?branch=develop)](https://coveralls.io/github/celestemiriams/Fast-Food-Fast-DB?branch=develop)

[![Maintainability](https://api.codeclimate.com/v1/badges/5ebd2e38383ea8d65fc0/maintainability)](https://codeclimate.com/github/celestemiriams/Fast-Food-Fast-DB/maintainability)

##   Project Title
    Fast-Food-Fast is an application that provides food delivery services for its users

### Features
- A user can create an account 
- A user can login with their credentials
- A user can make an order
- An admin can get a list of orders
- An admin can get a specific order
- An admin can update order status
- An admin can add menu options
- A user can get menu items

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequistes
Things you need to install and configure the software include: 
- Virtualenv
- Python3
- Flask
- pytest
-postgres

### Development setup
    
#### Create a virtual environment and activate it
```
 virtualenv venv
 source /env/bin/activate
```

#### Install dependencies
pip3 install -r requirements.txt

#### Run the application
```
cd Fast-Food-Fast
python run.py
```

#### You can access the application End points:
| End Point                    | Verb   | Use                            |
|:---------------------------- |:------:|:----------------------------------------------|
|/api/v1/auth/signup           |  POST	| Register a user                               |
|/api/v1/auth/login            |  POST	| Login a user                                  |
|/api/v1/users/orders/         |  POST	| Place an order for food                       |
|/api/v1/users/orders/         |  GET	| Get order history for a particular user       |
|/api/v1/orders/<int:order_id>/|  GET	| Get a specific order done by admin            |
|/api/v1/orders/               |  GET   | Get all orders done by admin                  |
|/api/v1/orders/<int:order_id>/|  PUT	| Update the status of an order                 |
|/api/v1/menu/                 |  POST  | Add meal option to the menu only done by admin|
|/api/v1/menu/                 |  GET   | Get available menu                            |


###  Running the Tests
```
    To run the tests run:
    pytest test_orders.py
```

###  Versioning
        For versions available check [tags on this repo](https://github.com/celestemiriams/Fast-Food-Fast-DB)

###   Authors
        *Nanteza Miriam

###   Acknowledgments
```
        LFA Arnold Taremwa
        kampala Bootcamp 12 fellows week2
        Andela development community
```
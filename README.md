# LabHamster 

Django project for simple purchase / order management, mostly targetted at
scientific labs. However, the work flow is very simple and generic:

   1. User A registers a product.
   2. User A or B creates an order for this product (status="pending").
   3. User C initiates the purchase (status="ordered")
   4. Whoever collects the item, sets the order status to "received".

The advantage for users A and B is that they can quickly figure out what the
state of their request is and that they, later, can quickly initiate
follow-up orders for the same product. The advantage for the purchase manager
C is that all the order requests are collected in one place, catalogue
numbers are required and prices or links as well as comments can be provided
by the user. There is a trail of who requested, who ordered and who received
an item and when. Filtering and full-text search facilitate finding products
or past orders. Products can be categorized and products and orders can be
exported as CSV tables for further processing in Excel.

Technically, LabHamster is a small and very standard Django project using not
much more than the out-of-the-box Django admin interface with a pretty
standard data model. 

## Setup your own LabHamster instance on Heroku

Click the following button to quickly spin up your very own instance of the LabHamster web server:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Fill out the form and your web server will be up and running in a minute. The app name you choose will be part of the default address, which will look like this: https://my-app-name.herokuapp.com. You can later easily connect this server to your own domain. The free configuration offered by heroku should be fine for the kind of teams that LabHamster is intended for. However, it needs to be inactive for at least 6h per day and there are a couple of seconds delay when the server hasn't been used since more than 30 min. These restrictions are removed if you upgrade to the "hobby" scheme (7 USD / month).

#### Modify and update a running heroku app
   
   - You can use the heroku dashboard to update your app directly from the labhamster.git repo.

   - To make changes to your LabHamster server, clone the app project locally using the [Heroku Toolbelt](https://toolbelt.heroku.com/):

      ```sh
      heroku login
      heroku git:clone --app YOURAPPNAME
      ```
   - ... and then update the heroku app from your local computer:

      ```sh
      cd YOURAPPNAME
      git remote add origin https://github.com/graik/labhamster
      git pull origin master # may trigger a few merge conflicts, depending on how long since last update
      git push heroku master
      ```
   - This latter option has the advantage, that you can test changes locally. See section [Setup for development].

## Getting started

1. Log in to the server with the `admin` user name and using labhamster2016 as your password. Then change the password by clicking the link in the upper left corner. You will find the database populated with two more example users (test_user and test_manager) and some example data and product categories. 
2. Log in with the "normal" test_user account as well as with the test_manager account (same password as above) to test the different permissions given to each of them.
3. Log in as admin and create a new user account. Assign the user to the  `labmember` group in order to give her or him basic permission to add and edit products, orders and vendor info.
4. Create a new user account and assign it to *both* `labmember` and `labmanager` group in order to give her or him the permission to create and change product categories, grants, and to also add new user accounts.
5. Once you have familiarized yourself with how all this works, delete the original test_user and test_manager users.

## Setup for development

Download, prepare virtual python environment and install dependencies (replace `git` by the `heroku clone` command from above if you want to start from a app deployed to heroku):
```shell
git clone https://github.com/graik/labhamster.git labhamsterdjango
cd labhamsterdjango
virtualenv venv
source venv/bin/activate
pip install -r requirements_local.txt
```
    
Create empty database tables (by default a very inefficient SQLite database,
modify `settings.py` to change that):
```
./manage.py migrate
```

Now create super user, recommended user name is "admin" (skip this step if you choose to load the example data 
in the next step): 
```
./manage.py createsuperuser
```

You can load a very small example data set into the database. This will
again create a super user "admin" with password labhamster2016:
```
./manage.py loaddata initial_data.json
```

Start Django's built-in debugging server:
```
./manage.py runserver
```

Point your web browser to http://127.0.0.1:8000 and enjoy!

## License

LabHamster is released open source under the [MIT license](./LICENSE).

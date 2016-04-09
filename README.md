# labhamster 

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

The project is released under the MIT open source license.

### Installation Instructions (for development)

Download, prepare virtual python environment and install dependencies:
```
git clone https://github.com/graik/labhamster.git labhamsterdjango
cd labhamsterdjango
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```
Create empty database tables (by default a very inefficient SQLite database, modify `settings.py` to change that).
```
./manage.py migrate
```
Now create super user, recommended user name is "admin" (if you want to load the example data in the next step):
```
./manage.py createsuperuser
```

You can load a very small example data set into the database. This will create one additional user "raik". 
```
./manage.py loaddata example_data.json
```

Start Django's built-in debugging server:
```
./manage.py runserver
```

Point your web browser to http://127.0.0.1:8000
and enjoy!


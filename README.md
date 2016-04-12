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

## Setup your own LabHamster instance on Heroku

A version of LabHamster configured for Heroku is currently kept on the github branch `heroku`. However, the changes don't seem to work just as well for the development server so I will probably soon merge this branch back into `master`. The following instructions assume you are sitting on a Ubuntu (or Debian-based) Linux machine. They should be pretty generic though.

1. Create a free Heroku account: https://signup.heroku.com/signup/dc
2. Install Heroku "tool belt":

   ```shell
   $ wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
   $ heroku login
   ```
   The `login` command will finish the installation.
   
3. Create a local copy of the LabHamster project.
   
   ```shell
   $ git clone https://github.com/graik/labhamster.git labhamsterdjango
   ```
   This will create a new folder `labhamsterdjango` in your current directory.
   
4. Create a heroku app.
   
   ```
   $ cd labhamsterdjango
   $ heroku login
      ... will ask for user name and password for your heroku account
   $ heroku create myown-labhamster
      ... some response text from heroku system
   $ heroku git:remote -a myown-labhamster
   ```
   Note: replace "myown-labhamster" by whatever name you like. Your web server will soon be live under `myown-labhamster.herokuapp.com`. The last `heroku git:remote` command is adding the heroku server 
   as an additional remote git repository. In theory, this should happen automatically during `heroku create`
   but sometimes it doesn't.

5. We are almost there! Now create your own secret key for https/ssh encryption:
   
   - generate new key at: http://www.miniwebtool.com/django-secret-key-generator/
   - replace any "(" or ")" by some other character
   ```sh
   $ heroku config:add DJANGO_SECRET_KEY="insert-your-secret-key-between-quotation-marks"
   ```
   - verify that the DJANGO_SECRET_KEY variable has been set: ```heroku config```

6. Last step: Push the LabHamster project (heroku branch) to your own heroku app instance
   
   ```sh
   $ git push heroku heroku:master
   ```
   That's it, well almost :)! Now you should see a bunch of compilation and deployment messages from heroku 
   (this may take a while), and finally something like this:
   ```
         remote: -----> Launching...
         remote: https://myown-labhamster.herokuapp.com/ deployed to Heroku
         remote: Verifying deploy... done.
         To https://git.heroku.com/myown-labhamster.git
         * [new branch] heroku -> master
   ```
   BTW, the `heroku:master` in the `git push` command is only needed because we are not using
   the `master` branch from the labhamster project. This will probably soon change.
   You can now inspect your shiny new LabHamster web server by going to: https://myown-labhamster.herokuapp.com.
   Or simply type: `heroku open` as a short-cut.
   There is only one little problem... we cannot login because we don't have any user account on 
   this server yet. Let's change that:
   ```
   $ heroku run ./manage.py createsuperuser
   ```
   This will now ask you for a user name and password for the super-user of your web server. 
   I recommend 'admin` as a user name.

7. Next steps.
   
   Your server is now live but empty. I have prepared two tiny data sets that should 
   make getting started easier. Load them by running the following command on your remote server:
   ```
   $ heroku run ./manage.py loaddata initial_usergroups.json
   $ heroku run ./manage.py loaddata initial_categories.json
   ```
   The first command will create two user groups: "labmember" and "labmanager". Any user that is part
   of the "labmember" group has the permission to file and modify products, orders and vendor records.
   Users that, *in addition*, are part of the "labmanager" group, moreover can create new user accounts,
   can create new categories or grants.
   
   The second data fixture contains some popular product categories, typical for a biolab. Any user
   with 'labmanager' permissions can change, delete or add categories through the web interface.
   
   In case things go wrong or out of curiosity, you should have a look at the log files of your web server.
   This is done with:
   
   ```
   $ heroku logs --tail
   ```
   The `--tail` will keep the log live, so that you can follow new entries arriving.

Further reading:
* https://devcenter.heroku.com/articles/django-app-configuration
* https://devcenter.heroku.com/articles/getting-started-with-python

## Setup Instructions for development

Download, prepare virtual python environment and install dependencies:
```shell
git clone https://github.com/graik/labhamster.git labhamsterdjango
cd labhamsterdjango
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
    
Create empty database tables (by default a very inefficient SQLite database,
modify `settings.py` to change that):
```
./manage.py migrate
```

Now create super user, recommended user name is "admin" (if you want to load
the example data in the next step): 
```
./manage.py createsuperuser
```

You can load a very small example data set into the database. This will
create one additional user "raik":
```
./manage.py loaddata example_data.json
```

Start Django's built-in debugging server:
```
./manage.py runserver
```

Point your web browser to http://127.0.0.1:8000 and enjoy!


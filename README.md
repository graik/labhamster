# labhamster
Django project for simple purchase / order management in scientific labs

Labhamster is a simple Django project for tracking materials and reagents ordered for a scientific laboratory 
and offers a rudimentary inventory management. For now it is not much more than the out-of-the-box Django 
admin interface with a pretty standard data model.

### Installation Instructions
(for quick evaluation, debugging & development)

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

Point your web browser to http://127.0.0.1:9000/admin
and enjoy!


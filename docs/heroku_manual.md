## Manual setup for Heroku *and* development

The following instructions assume you are sitting on a Ubuntu (or Debian-based) Linux machine. They should be pretty generic though. Before you start, make sure [Python](http://python.org) and [Git](http://git.org) are installed on your machine.

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
   new categories or grants.
   
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

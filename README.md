# URL-Shortener
This repository implements a simple URL shortener using Python's Flask.

In order for this project to correctly run you must install the following packages:
* `pip3 install flask`
* `pip3 install flask-sqlalchemy`

The next step is to create the database that will be used for inserting URLs:
* `$ python3`
* `>>> from app import db`
* `>>> db.create_all()`
* `>>> exit()`

Now all you have to do is run the `app.py` file and direct yourself to:
* `http://localhost:5000/`

Once there, enter in the URL you would like to be shortened and you will be redirected to a page displaying your newly shortened URL. Clicking on this new link will direct you to the original URL you entered in the intial form.

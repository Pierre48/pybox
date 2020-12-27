# pybox

## Quickstart for development
Firt, get source files, and install requirements : 
````
git clone https://github.com/gothinkster/flask-realworld-example-app.git
cd flask-realworld-example-app
pip install -r requirements/dev.txt
````
Set Flask environment variables : 
````
export FLASK_APP=/path/to/autoapp.py
export FLASK_DEBUG=1
export CONDUIT_SECRET='something-really-secret'
````

Next, create DB and its elements
````
flask db init
flask db migrate
flask db upgrade
````

You can now run the development server
````
flask run --with-threads
````

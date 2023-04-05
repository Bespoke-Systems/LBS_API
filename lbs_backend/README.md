# Nipate API's

### Project Local Development Setup

```bash
# create a python 3.8+ virtualenv
$ python3 -m venv [name-of-your-env]
$ source [name-of-env]/bin/activate

# navigate to project folder
$ cd lbs_backend

# install the required dependencies in your env
$ pip install -r requeirements.txt
$ cd lbs_backend

# migrate your sqlite3 database
$ python manage.py migrate
$ python manage runserver
$ python manage.py locations --app_name=locations
```

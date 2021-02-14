
FSND Capstone project
=====================

### General specifications

[Rubric](https://review.udacity.com/#!/rubrics/2682/view): It is required to build an API service and host it on Heroku.

1. Database
    - At least two classes (tables)
    - Each with a primary key
    - At least two attributes each (columns)
    - o2m or m2m relationship between the classes
        - queries should be exclusively performed through SQLAlchemy, not SQL
        - create methods to serialize model data
        - create helper methods to simplify API behavior such as insert, update and delete
1. Tests
    - One test for success behavior of each endpoint
    - One test for error behavior of each endpoint
    - At least two tests of RBAC for each role
1.  Endpoints
    - Two GET requests
    - One POST request
    - One PATCH request
    - One DELETE request
1. Roles
    - Two roles with different permissions
    - **Permissions specified for all endpoints**

---

- [x] Setup a remote Git [repository](https://github.com/AlFX/FSND_capstone)
- [x] Setup the database
    - [x] Create a database using `createdb <name>` in `postgres`
    - [x] Establish a connection to the database, add its URI to `config.py`
    - [x] Create the table models and estabilish relationships among them
    - [x] Create the database table running the migrations
        ```bash
        flask db init
        flask db migrate
        flask db upgrade
        ```
        if iteration is needed, reset the database as follows within `postgres`:
        ```bash
        dropdb <name> && createdb <name>
        ```
    - [x] Seed the database with `populate.py` and `dummy_data.py`
- [ ] Write the tests for the routes
- [ ] Write the basic app factory function in `__init__.py`
- [ ] Write the routes which can either serve as API or to display views
    - If a frontend is needed, write the HTML, CSS and Javascript for the views
    - Remeber: they must satisfy the tests!
- [ ] Test an alternative `models.py` file to make the relationships uniform, either using `backref` or `back_populates` but not both!
- [ ] **Run the app**: `FLASK_APP=app.py FLASK_DEBUG=true flask run`
- [ ] Setup the [roles](auth0.com)
- [ ] Deploy to [Heroku](dashboard.heroku.com)

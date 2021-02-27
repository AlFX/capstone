
Casting Agency API
==================

Assign actors to upcoming movies and keep track of their careers.


### Model Classes

These API are made of the following classes:

- **Movie**: it has one or more Genres and Actors and holds information about the release date and is related to Actors through the Interpretation model
- **Genre**: it is a list of possible genres for the Movies
- **Actor**: it holds basic Actors information like date of birth and gender has well as a list of the starred Movies through the Interpretation model
- **Interpretation**: this is an Association Object correlating multiple Actors to multiple Movies, holding information about the character potrayed by an Actor in a specific Movie


### Roles and Permissions

There are three roles supported by Roles Based Access Control (RBAC): Casting Assistant, Casting Director and Executive Producer.

There is no public access to data.

- **Casting Assistant**: can only view movies and actors data
- **Casting Director**: in addition to the Casting Assistant's permissions, he can add or delete an actor from the database and modify actors or movies
- **Executive Producer**: in addition to the Casting Director's permissions, he can add or delete a movie from the database


### Authorization

The project has been set up to authenticate using Auth0 Javascript Web Tokens (JWT). These are set up and signed with Auth0's private key. Their validity can be checked (by anyone) using their public keys.

Three users have been set up in Auth0 to use the Casting Agency API, a Casting Assistant, a Casting Director and an Executive Producer, who each have the necessary permissions to carry out typical tasks for each role.

Three JWT are provided for the above roles. These have been included in the `setup.sh` file, provided separately.


### A note for Mentors

**There is no way to set browser-based flows tokens maximum expiration time beyond 24 hours!**


### Live deployment

Run requests using cURL or Postman against [this URL](https://fsnd-capstone-alfx.herokuapp.com/), using the tokens provided in the `setup.sh` file.


### Running the server locally

Create a virtual environment and from within, run:
```bash
source setup.sh                             # set environment variables needed by Auth0 and the Flask app
python -m pip install --upgrade pip         # make sure to run PIP latest version
python -m pip install -r requirements.txt   # install dependencies
```

Once done the above, setup and populate the database as follows:
```bash
flask db init          # initialize the migrations
flask db migrate       # detect the changes in the database tables
flask db upgrade       # create/update the database schema
python populate        # populate the database with toy data
```


### Running the test suite locally

Make sure that `setup.sh` has been sourced as per previous instruction (this, among other things will setup the needed JWTs as local environment variables), then launch the test suite from the project route directory as shown:
```bash
python -m tests.runner
```

### Endpoint conventions and Error codes

### API endpoints

Below are all the endpoints with a brief description:

| Method | Route                        | Description               |
| ------ | ---------------------------- | ------------------------- |
| GET    | `/`                          | Landing page              |
| GET    | `/movies`                    | Returns a list of movies  |
| GET    | `/movies/<movie_id>`         | Returns a single movie    |
| POST   | `/movies/add`                | Add a single movie        |
| PATCH  | `/movies/update/<movie_id>`  | Update a single movie     |
| DELETE | `/movies/delete/<movie_id>`  | Delete a single movie     |
| GET    | `/genres`                    | Returns a list of genres  |
| GET    | `/genres/<genre_id>`         | Returns a single genre    |
| GET    | `/actors`                    | Returns a list of actors  |
| GET    | `/actors/<actor_id>`         | Returns a single actor    |
| POST   | `/actors/add`                | Add a single actor        |
| PATCH  | `/actors/update/<actor_id>`  | Update a single actor     |

#### `GET /`

- Displays the home page with this API documentation. Not intended to be called by API clients.
- Request Arguments: None
- Returns: Rendered HTML


#### `GET /movies`


#### `GET /movies/<movie_id>`


#### `POST /movies/add`


#### `PATCH /movies/update/<movie_id>`


#### `DELETE /movies/delete/<movie_id>`


#### `GET /genres`


#### `GET /genres/<genre_id>`


#### `GET /actors`


#### `GET /actors/<actor_id>`


#### `POST /actors/add`


#### `PATCH /actors/update/<actor_id>`



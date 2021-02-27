
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
flask db init                               # initialize the migrations
flask db migrate                            # detect the changes in the database tables
flask db upgrade                            # create/update the database schema
python populate.py                          # launch a script to populate the database with toy data
```


### Running the test suite locally

Make sure that `setup.sh` has been sourced as per previous instruction (this, among other things will setup the needed JWTs as local environment variables), then launch the test suite from the project route directory as shown:
```bash
python -m tests.runner
```

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

- Displays the home page
- Available to anyone
- Request Arguments: None
- Returns: Rendered HTML


#### `GET /movies`

- Displays the whole list of movies
- Available to all roles
- Request Arguments: None
- Returns: json data

```json
{
    "movie": [
        {
            "genre": [
                "Drama",
                "Romance"
            ],
            "interpretation": {
                "Humphrey Bogart": "Rick Blaine",
                "Ingrid Bergman": "Ilsa Lund"
            },
            "release_date": "Thu, 26 Nov 1942 00:00:00 GMT",
            "title": "Casablanca"
        },

        ... truncated for brevity ...

        {
            "genre": [
                "Crime"
            ],
            "interpretation": {
                "Humphrey Bogart": "maj. Frank McCloud",
                "Lauren Bacall": "Nora Temple"
            },
            "release_date": "Thu, 01 Jan 1948 00:00:00 GMT",
            "title": "Key Largo"
        }
    ],
    "success": true
}
```

#### `GET /movies/<movie_id>`

- Displays a single movie
- Available to all roles
- Request Arguments: movie id
- Returns: json data

```json
{
    "movie": {
        "genre": [
            "Drama",
            "Romance"
        ],
        "interpretation": {
            "Humphrey Bogart": "Rick Blaine",
            "Ingrid Bergman": "Ilsa Lund"
        },
        "release_date": "Thu, 26 Nov 1942 00:00:00 GMT",
        "title": "Casablanca"
    },
    "success": true
}
```

#### `POST /movies/add`

- Adds a single movie to the database
- Available to the Executive Producer role only
- Request Arguments: json data (title, publication date)
- Returns: json data

```json
{
    "added": <new_movie.id>,
    "success": true
}
```

#### `PATCH /movies/update/<movie_id>`

- Edits a single movie to the database
- Available to the Casting Director and Executive Producer roles only
- Request Arguments: movie id
- Returns: json data

```json
{
    "updated": <movie.id>,
    "success": true
}
```

#### `DELETE /movies/delete/<movie_id>`

- Deletes a single movie to the database
- Available to the Executive Producer role only
- Request Arguments: movie id
- Returns: json data

```json
{
    "deleted": <movie.id>,
    "success": true
}
```

#### `GET /genres`

- Displays the whole list of genres
- Available to all roles
- Request Arguments: None
- Returns: json data

```json
{
    "genre": [

        ... truncated for brevity ...

        {
            "movies": [
                "The Big Sleep",
                "The Maltese Falcon",
                "Key Largo"
            ],
            "name": "Crime"
        },
        {
            "movies": [
                "Casablanca"
            ],
            "name": "Drama"
        },

        ... truncated for brevity ...

    ],
    "success": true
}
```


#### `GET /genres/<genre_id>`

- Displays a single genre
- Available to all roles
- Request Arguments: genre id
- Returns: json data

```json
{
    "genre": {
        "movies": [
            "The Big Sleep",
            "The Maltese Falcon",
            "Key Largo"
        ],
        "name": "Crime"
    },
    "success": true
}
```


#### `GET /actors`

- Displays the whole list of actors
- Available to all roles
- Request Arguments: None
- Returns: json data

```json
{
    "actor": [
        {
            "dob": "Mon, 25 Dec 1899 00:00:00 GMT",
            "filmography": {
                "Casablanca": "Rick Blaine",
                "Key Largo": "maj. Frank McCloud",
                "Sabrina": "Linus Larrabee",
                "The Big Sleep": "Philip Marlowe",
                "The Maltese Falcon": "Sam Spade"
            },
            "gender": "male",
            "name": "Humphrey",
            "surname": "Bogart"
        },

        ... truncated for brevity ...

        {
            "dob": "Thu, 28 May 1925 00:00:00 GMT",
            "filmography": {
                "The Big Sleep": "Carmen Sternwood"
            },
            "gender": "female",
            "name": "Martha",
            "surname": "Vickers"
        }
    ],
    "success": true
```


#### `GET /actors/<actor_id>`

- Displays a single actor
- Available to all roles
- Request Arguments: actor id
- Returns: json data

```json
{
    "actor": {
        "dob": "Mon, 25 Dec 1899 00:00:00 GMT",
        "filmography": {
            "Casablanca": "Rick Blaine",
            "Key Largo": "maj. Frank McCloud",
            "Sabrina": "Linus Larrabee",
            "The Big Sleep": "Philip Marlowe",
            "The Maltese Falcon": "Sam Spade"
        },
        "gender": "male",
        "name": "Humphrey",
        "surname": "Bogart"
    },
    "success": true
}
```

#### `POST /actors/add`

- Add a single actor to the database
- Available to the Casting Director and Executive Producer roles only
- Request Arguments: actor data (name, surname, date of birth, gender)
- Returns: json data

```json
{
    "added": <actor.id>,
    "success": true
}
```

#### `PATCH /actors/update/<actor_id>`

- Edits a single actor from the database
- Available to the Casting Director and Executive Producer roles only
- Request Arguments: actor id
- Returns: json data

```json
{
    "updated": <actor.id>,
    "success": true
}
```

#### `DELETE /actors/delete/<actor_id>`

- Deletes a single actor from the database
- Available to the Casting Director and Executive Producer roles only
- Request Arguments: actor id
- Returns: json data

```json
{
    "deleted": <actor.id>,
    "success": true
}
```

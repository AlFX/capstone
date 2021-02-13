movies = [
    {
        'id': 1,
        'title': 'Casablanca',
        'release_date': '1942-11-26',
    },
    {
        'id': 2,
        'title': 'The Big Sleep',
        'release_date': '1946-01-01',
    },
    {
        'id': 3,
        'title': 'Sabrina',
        'release_date': '1954-01-01',
    },
    {
        'id': 4,
        'title': 'The Maltese Falcon',
        'release_date': '1941-01-01',
    },
    {
        'id': 5,
        'title': 'Key Largo',
        'release_date': '1948-01-01',
    },
]

genres = {
    'Action': 1,
    'Animation': 2,
    'Comedy': 3,
    'Crime': 4,
    'Drama': 5,
    'Experimental': 6,
    'Fantasy': 7,
    'Historical': 8,
    'Horror': 9,
    'Romance': 10,
    'Science Fiction': 11,
    'Thriller': 12,
    'Western': 13,
    'Other': 14
}

actors = [
    {
        'id': 1,
        'name': 'Humphrey',
        'surname': 'Bogart',
        'dob': '1899-12-25',
        'gender': 'male'
    },
    {
        'id': 2,
        'name': 'Lauren',
        'surname': 'Bacall',
        'dob': '1924-09-16',
        'gender': 'female'
    },
    {
        'id': 3,
        'name': 'Audrey',
        'surname': 'Hepburn',
        'dob': '1929-01-01',
        'gender': 'female'
    },
    {
        'id': 4,
        'name': 'Bill',
        'surname': 'Holden',
        'dob': '1918-01-01',
        'gender': 'male'
    },
    {
        'id': 5,
        'name': 'Ingrid',
        'surname': 'Bergman',
        'dob': '1915-08-29',
        'gender': 'female'
    },
    {
        'id': 6,
        'name': 'Martha',
        'surname': 'Vickers',
        'dob': '1925-05-28',
        'gender': 'female'
    },
]

interpretations = [
    {
        'movie_id': 1,
        'actor_id': 1,
        'character': 'Rick Blaine'
    },
    {
        'movie_id': 2,
        'actor_id': 1,
        'character': 'Philip Marlowe'
    },
    {
        'movie_id': 3,
        'actor_id': 1,
        'character': 'Linus Larrabee'
    },
    {
        'movie_id': 4,
        'actor_id': 1,
        'character': 'Sam Spade'
    },
    {
        'movie_id': 5,
        'actor_id': 1,
        'character': 'maj. Frank McCloud'
    },
    {
        'movie_id': 2,
        'actor_id': 2,
        'character': 'Vivian Sternwood Rutledge'
    },
    {
        'movie_id': 5,
        'actor_id': 2,
        'character': 'Nora Temple'
    },
    {
        'movie_id': 2,
        'actor_id': 6,
        'character': 'Carmen Sternwood'
    },
    {
        'movie_id': 1,
        'actor_id': 5,
        'character': 'Ilsa Lund'
    },
    {
        'movie_id': 3,
        'actor_id': 4,
        'character': 'David Larrabee'
    },
    {
        'movie_id': 3,
        'actor_id': 3,
        'character': 'Sabrina Fairchild'
    },
]

movie_genre_association = [
    {
        'movie_id': 1,
        'genre_id': 10,
    },
    {
        'movie_id': 1,
        'genre_id': 5,
    },
    {
        'movie_id': 2,
        'genre_id': 4,
    },
    {
        'movie_id': 4,
        'genre_id': 4,
    },
    {
        'movie_id': 5,
        'genre_id': 4,
    },
    {
        'movie_id': 3,
        'genre_id': 3,
    },
    {
        'movie_id': 3,
        'genre_id': 10,
    },
]

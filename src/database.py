import sqlite3

DB_NAME = 'movies.db'


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn


def create_table():
    """اگر جدول فیلم‌ها وجود نداشته باشد آن را می‌سازد"""
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            rating      REAL    NOT NULL,
            year        INTEGER NOT NULL,
            country     TEXT    NOT NULL,
            image_path  TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_movie(name, rating, year, country):
    conn = get_connection()
    cur = conn.execute(
        'INSERT INTO movies (name, rating, year, country) VALUES (?, ?, ?, ?)',
        (name, rating, year, country)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_movie(movie_id):
    conn = get_connection()
    row = conn.execute('SELECT * FROM movies WHERE id = ?', (movie_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_movies(country=None, year=None, min_rating=None, name=None):
    """همه فیلم‌ها؛ با فیلتر اختیاری روی کشور، سال، حداقل امتیاز و بخشی از نام"""
    query = 'SELECT * FROM movies WHERE 1=1'
    params = []

    if country is not None:
        query += ' AND LOWER(country) = LOWER(?)'
        params.append(country)
    if year is not None:
        query += ' AND year = ?'
        params.append(year)
    if min_rating is not None:
        query += ' AND rating >= ?'
        params.append(min_rating)
    if name is not None:
        query += ' AND name LIKE ?'
        params.append(f'%{name}%')

    query += ' ORDER BY id'

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_movie(movie_id, name, rating, year, country):
    conn = get_connection()
    cur = conn.execute(
        'UPDATE movies SET name = ?, rating = ?, year = ?, country = ? WHERE id = ?',
        (name, rating, year, country, movie_id)
    )
    conn.commit()
    changed = cur.rowcount
    conn.close()
    return changed > 0


def set_image_path(movie_id, image_path):
    conn = get_connection()
    conn.execute('UPDATE movies SET image_path = ? WHERE id = ?', (image_path, movie_id))
    conn.commit()
    conn.close()


def delete_movie(movie_id):
    conn = get_connection()
    cur = conn.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return deleted > 0

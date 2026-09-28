import os
import shutil
from typing import Optional

from fastapi import HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi_offline import FastAPIOffline
from pydantic import BaseModel, Field

import database

app = FastAPIOffline()

IMAGES_DIR = 'images'
os.makedirs(IMAGES_DIR, exist_ok=True)

database.create_table()

class Movie(BaseModel):
    name: str = Field(min_length=1)
    rating: float = Field(ge=0, le=10)
    year: int = Field(ge=1888, le=2100)
    country: str = Field(min_length=1)


def get_movie_or_404(movie_id: int):
    movie = database.get_movie(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f'Movie {movie_id} not found')
    return movie

@app.get('/')
def get_index():
    return {'HELLO': 'MOVIES API'}


@app.post('/movies/', status_code=201)
def add_movie(movie: Movie):
    new_id = database.insert_movie(movie.name, movie.rating, movie.year, movie.country)
    return {'message': 'movie added', 'movie': database.get_movie(new_id)}

@app.get('/movies/')
def get_movies(
    country: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = None,
    name: Optional[str] = None,
):
    return {'movies': database.get_all_movies(country, year, min_rating, name)}


@app.get('/movies/{movie_id}')
def get_movie(movie_id: int):
    return get_movie_or_404(movie_id)


@app.put('/movies/{movie_id}')
def update_movie(movie_id: int, movie: Movie):
    get_movie_or_404(movie_id)
    database.update_movie(movie_id, movie.name, movie.rating, movie.year, movie.country)
    return {'message': 'movie updated', 'movie': database.get_movie(movie_id)}


@app.delete('/movies/{movie_id}')
def delete_movie(movie_id: int):
    movie = get_movie_or_404(movie_id)

    if movie['image_path'] and os.path.exists(movie['image_path']):
        os.remove(movie['image_path'])

    database.delete_movie(movie_id)
    return {'message': f'movie {movie_id} deleted'}


@app.post('/movies/{movie_id}/image')
def upload_image(movie_id: int, file: UploadFile = File(...)):
    movie = get_movie_or_404(movie_id)

    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='File must be an image')


    if movie['image_path'] and os.path.exists(movie['image_path']):
        os.remove(movie['image_path'])

    ext = os.path.splitext(file.filename)[1].lower() or '.jpg'
    image_path = os.path.join(IMAGES_DIR, f'movie_{movie_id}{ext}')

    with open(image_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    database.set_image_path(movie_id, image_path)
    return {'message': 'image saved', 'image_path': image_path}


@app.get('/movies/{movie_id}/image')
def get_image(movie_id: int):
    movie = get_movie_or_404(movie_id)

    if not movie['image_path'] or not os.path.exists(movie['image_path']):
        raise HTTPException(status_code=404, detail='This movie has no image')

    return FileResponse(movie['image_path'])

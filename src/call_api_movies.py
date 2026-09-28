import requests

BASE_URL = 'http://127.0.0.1:8000'


def add_movie(name, rating, year, country):
    data = {'name': name, 'rating': rating, 'year': year, 'country': country}
    response = requests.post(f'{BASE_URL}/movies/', json=data)

    if response.status_code != 201:
        return 'ERROR', response.text
    return response.json()


def get_all_movies(country=None, year=None, min_rating=None, name=None):
    params = {
        'country': country,
        'year': year,
        'min_rating': min_rating,
        'name': name,
    }
    
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(f'{BASE_URL}/movies/', params=params)

    if response.status_code != 200:
        return 'ERROR', response.text
    return response.json()


def get_movie(movie_id):
    response = requests.get(f'{BASE_URL}/movies/{movie_id}')

    if response.status_code != 200:
        return 'ERROR', response.text
    return response.json()


def update_movie(movie_id, name, rating, year, country):
    data = {'name': name, 'rating': rating, 'year': year, 'country': country}
    response = requests.put(f'{BASE_URL}/movies/{movie_id}', json=data)

    if response.status_code != 200:
        return 'ERROR', response.text
    return response.json()


def delete_movie(movie_id):
    response = requests.delete(f'{BASE_URL}/movies/{movie_id}')

    if response.status_code != 200:
        return 'ERROR', response.text
    return response.json()


def upload_image(movie_id, image_file_path):
    with open(image_file_path, 'rb') as f:
        files = {'file': (image_file_path, f, 'image/jpeg')}
        response = requests.post(f'{BASE_URL}/movies/{movie_id}/image', files=files)

    if response.status_code != 200:
        return 'ERROR', response.text
    return response.json()


def download_image(movie_id, save_as):
    response = requests.get(f'{BASE_URL}/movies/{movie_id}/image')

    if response.status_code != 200:
        return 'ERROR', response.text

    with open(save_as, 'wb') as f:
        f.write(response.content)
    return f'image saved as {save_as}'


if __name__ == '__main__':
    print(add_movie('Inception', 8.8, 2010, 'USA'))
    print(add_movie('A Separation', 8.3, 2011, 'Iran'))
    print(get_all_movies())
    print(get_all_movies(country='Iran'))
    print(update_movie(1, 'Inception', 9.0, 2010, 'USA'))
    # print(upload_image(1, 'inception.jpg'))
    # print(download_image(1, 'downloaded.jpg'))
    # print(delete_movie(2))

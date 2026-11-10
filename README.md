# Movies API

یک API ساده برای مدیریت فیلم‌ها با FastAPI و SQLite.

## ویژگی‌ها

- افزودن، دریافت، ویرایش و حذف فیلم
- فیلتر فیلم‌ها بر اساس کشور، سال، حداقل امتیاز و نام
- آپلود و دریافت تصویر برای هر فیلم
- دیتابیس SQLite
- کلاینت نمونه برای تست API

## ساختار پروژه

```
├── app_movie.py          # سرور FastAPI
├── database.py           # عملیات دیتابیس SQLite
├── call_api_movies.py    # اسکریپت کلاینت برای تست API
├── images/               # پوشه ذخیره تصاویر فیلم‌ها (خودکار ساخته می‌شود)
└── movies.db             # فایل دیتابیس (خودکار ساخته می‌شود)
```

## پیش‌نیازها

- پایتون ۳.۸ یا بالاتر

## نصب وابستگی‌ها

```bash
pip install fastapi uvicorn pydantic python-multipart requests fastapi-offline
```

> نکته: `fastapi-offline` برای اجرا بدون نیاز به اینترنت استفاده شده. اگر نمی‌خواهید از آن استفاده کنید، می‌توانید به `from fastapi import FastAPI` تغییر دهید.

## اجرای سرور

```bash
uvicorn app_movie:app --reload
```

سرور روی آدرس زیر اجرا می‌شود:

```
http://127.0.0.1:8000
```

مستندات خودکار (Swagger UI):

```
http://127.0.0.1:8000/docs
```

## اندپوینت‌ها

| متد    | مسیر                      | توضیح                          |
|--------|---------------------------|--------------------------------|
| GET    | `/`                       | پیام خوش‌آمدگویی               |
| POST   | `/movies/`                | افزودن فیلم جدید               |
| GET    | `/movies/`                | لیست فیلم‌ها (با فیلتر اختیاری)|
| GET    | `/movies/{movie_id}`      | دریافت یک فیلم                 |
| PUT    | `/movies/{movie_id}`      | ویرایش فیلم                    |
| DELETE | `/movies/{movie_id}`      | حذف فیلم                       |
| POST   | `/movies/{movie_id}/image`| آپلود تصویر فیلم               |
| GET    | `/movies/{movie_id}/image`| دریافت تصویر فیلم              |

### پارامترهای فیلتر در `GET /movies/`

- `country` : کشور (مثلاً `Iran`)
- `year` : سال ساخت
- `min_rating` : حداقل امتیاز
- `name` : بخشی از نام فیلم

### مدل فیلم

```json
{
  "name": "Inception",
  "rating": 8.8,
  "year": 2010,
  "country": "USA"
}
```

- `name`: حداقل ۱ کاراکتر
- `rating`: بین ۰ تا ۱۰
- `year`: بین ۱۸۸۸ تا ۲۱۰۰
- `country`: حداقل ۱ کاراکتر

## تست با کلاینت

بعد از اجرای سرور، اسکریپت کلاینت را اجرا کنید:

```bash
python call_api_movies.py
```

این اسکریپت چند فیلم اضافه می‌کند، لیست می‌گیرد، فیلتر می‌کند و یک فیلم را ویرایش می‌کند.

توابع موجود در کلاینت:

- `add_movie(name, rating, year, country)`
- `get_all_movies(country=None, year=None, min_rating=None, name=None)`
- `get_movie(movie_id)`
- `update_movie(movie_id, name, rating, year, country)`
- `delete_movie(movie_id)`
- `upload_image(movie_id, image_file_path)`
- `download_image(movie_id, save_as)`

## مثال درخواست‌ها با curl

**افزودن فیلم:**
```bash
curl -X POST http://127.0.0.1:8000/movies/ \
  -H "Content-Type: application/json" \
  -d '{"name": "A Separation", "rating": 8.3, "year": 2011, "country": "Iran"}'
```

**گرفتن همه فیلم‌ها:**
```bash
curl http://127.0.0.1:8000/movies/
```

**فیلتر بر اساس کشور:**
```bash
curl "http://127.0.0.1:8000/movies/?country=Iran"
```

**آپلود تصویر:**
```bash
curl -X POST http://127.0.0.1:8000/movies/1/image \
  -F "file=@poster.jpg"
```

## نکات

- تصاویر در پوشه `images/` ذخیره می‌شوند.
- هنگام حذف فیلم، تصویر مربوطه هم پاک می‌شود.
- دیتابیس به صورت خودکار ساخته می‌شود.

## مجوز

این پروژه برای استفاده آموزشی و شخصی آزاد است.

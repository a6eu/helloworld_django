from site_market.celery import app
import requests
from decimal import Decimal
from .models import Product
from brand.models import Brand
from category.models import Category
from django.core.files import File
import json
import os


@app.task()
def update_products():
    # url = "https://b2b.marvel.kz/Api/GetFullStock"
    # params = {
    #     "user": "01itgroup04",
    #     "password": "m_u_oOV8N1",
    #     "secretKey": "",
    #     "packStatus": 0,
    #     "responseFormat": 1,
    #     "instock": 0,
    #     "updatedSince": "24072019"
    # }
    # response = requests.post(url, params=params)
    # if response.status_code == 200:
    #     try:
    #         data = response.json()
    #     except ValueError:
    #         data = None
    json_file_path = '~/Downloads/Telegram Desktop/responseStock.json'
    json_file_path = os.path.expanduser(json_file_path)

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл не найден: {json_file_path}")
        return

    if data and 'Body' in data and 'CategoryItem' in data['Body']:
        products_data = data['Body']['CategoryItem']
        for product_data in products_data:
            save_product(product_data)
    else:

        print("Нет данных для обработки или неверный формат данных.")


@app.task()
def update_product_images():
    articles = Product.objects.values_list('article', flat=True).distinct()
    items = [{'ItemId': article} for article in articles if article]

    url = "https://b2b.marvel.kz/Api/GetItemPhotos"
    data = {
        "user": "01itgroup04",
        "password": "m_u_oOV8N1",
        "responseFormat": 1,
        "items": {"WareItem": items}
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            print("Ошибка: Полученный ответ не является валидным JSON.")
            return

        if data and 'Body' in data and 'Photo' in data['Body']:
            photos_data = data['Body']['Photo']
            already_updated = set()  # Для отслеживания уже обновленных артикулов

            for photo in photos_data:
                big_image = photo.get('BigImage', {})
                ware_article = big_image.get('WareArticle')

                if ware_article not in already_updated:
                    img_url = big_image.get('URL')
                    if img_url:
                        Product.objects.filter(article=ware_article).update(img_url=img_url)
                        already_updated.add(ware_article)
        else:
            print("Ошибка: Ответ от API не содержит ожидаемых данных.")
    else:
        print(f"Ошибка: Статус ответа API - {response.status_code}")


def save_product(product_data):
    category_id = product_data.get('CategoryId')
    brand_name = product_data.get('WareVendor')

    try:
        category = Category.objects.get(categoryId=category_id)
    except Category.DoesNotExist:
        return

    brand, _ = Brand.objects.get_or_create(name=brand_name)

    quantity_str = product_data.get('TotalInventQty', '0')
    if quantity_str.endswith('+'):
        quantity_str = quantity_str[:-1]
    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 0

    product, created = Product.objects.update_or_create(
        name=product_data.get('WareFullName'),
        defaults={
            'price': Decimal(product_data.get('WarePriceKZT').replace(',', '.')),
            'description': '',
            'rating_total': 0,
            'category': category,
            'brand': brand,
            'quantity': quantity,
            'article': product_data.get('WareArticle')
            # 'img_url':
        }
    )

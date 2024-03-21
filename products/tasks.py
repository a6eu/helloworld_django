from site_market.celery import app
import requests
from decimal import Decimal, InvalidOperation
from .models import Product
from brand.models import Brand
from category.models import Category
from django.core.files import File
import json
import os
import xml.etree.ElementTree as ET


@app.task()
def update_products():
    url = "https://b2b.marvel.kz/Api/GetFullStock"
    params = {
        "user": "01itgroup04",
        "password": "m_u_oOV8N1",
        "secretKey": "",
        "packStatus": 0,
        "responseFormat": 1,
        "instock": 0,
        "updatedSince": "24072019"
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            data = None
    json_file_path = '~/Downloads/Telegram Desktop/responseStock.json'
    json_file_path = os.path.expanduser(json_file_path)

    # try:
    #     with open(json_file_path, 'r') as file:
    #         data = json.load(file)
    # except FileNotFoundError:
    #     print(f"Файл не найден: {json_file_path}")
    #     return

    if data and 'Body' in data and 'CategoryItem' in data['Body']:
        products_data = data['Body']['CategoryItem']
        for product_data in products_data:
            save_product(product_data)
    else:

        print("Нет данных для обработки или неверный формат данных.")


@app.task()
def update_product_images():
    items = Product.objects.values_list('article', flat=True).distinct()

    root = ET.Element("Root")
    for item in items:
        if item:
            ware_item = ET.SubElement(root, "WareItem")
            item_id = ET.SubElement(ware_item, "ItemId")
            item_id.text = item

    xml_data = ET.tostring(root, encoding='unicode')

    url = "https://b2b.marvel.kz/Api/GetItemPhotos"
    params = {
        'user': '01itgroup04',
        'password': 'm_u_oOV8N1',
        'responseFormat': 1,
        'items': xml_data
    }

    response = requests.post(url, json=params)
    if response.status_code == 200:
        try:
            json_data = response.json()
        except ValueError:
            print("Ошибка: Полученный ответ не является валидным JSON.")
            return

        # Обработка ответа и обновление img_url в базе данных
        if json_data and 'Body' in json_data and 'Photo' in json_data['Body']:
            for photo in json_data['Body']['Photo']:
                big_image = photo.get('BigImage', {})
                ware_article = big_image.get('WareArticle')
                img_url = big_image.get('URL')
                if img_url and ware_article:
                    Product.objects.filter(article=ware_article).update(img_url=img_url)
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
    price_str = product_data.get('WarePriceKZT', '0').replace(',', '.')
    try:
        price = Decimal(price_str)
    except (InvalidOperation, ValueError):
        price = Decimal('0')

    if price <= 0:
        return

    # Create or update the product
    product, created = Product.objects.update_or_create(
        name=product_data.get('WareFullName'),
        defaults={
            'price': price,
            'description': '',
            'rating_total': 0,
            'category': category,
            'brand': brand,
            'quantity': quantity,
            'article': product_data.get('WareArticle')
            # 'img_url':  # Add image URL handling if required
        }
    )

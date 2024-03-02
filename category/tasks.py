from celery import shared_task
import requests
from .models import Category
from site_market.celery import app


# @app.task
# def test_task():
#     print('Worked')
#     return True

@app.task()
def update_categories():
    url = "https://b2b.marvel.kz/Api/GetCatalogCategories"
    data = {
        "user": "01itgroup04",
        "password": "m_u_oOV8N1",
        "secretKey": "",
        "responseFormat": 1
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        categories_data = response.json().get('Body', {}).get('Categories', [])
        for category_data in categories_data:
            if category_data['CategoryName'] in ["Персональные компьютеры", "Ноутбуки и планшеты",
                                                 "Мониторы и профессиональные панели"]:
                save_category(category_data)


def save_category(category_data, parent=None):
    category, created = Category.objects.get_or_create(
        categoryId=category_data['CategoryID'],
        defaults={
            'name': category_data['CategoryName'],
            'parent': parent
        }
    )

    for subcategory_data in category_data.get('SubCategories', []):
        save_category(subcategory_data, parent=category)

# @app.task()
# def update_database():
#     api_url = 'https://b2b.marvel.kz/Api/GetCatalogCategories'
#     payload = {
#         'user': '01itgroup04',
#         'password': 'm_u_oOV8N1',
#         'secretKey': '',
#         'responseFormat': 1
#     }
#
#     response = requests.post(api_url, data=payload)
#
#     if response.status_code == 200:
#         try:
#             data = response.json()
#             if data is not None and 'Body' in data and 'Categories' in data['Body']:
#                 categories = data['Body']['Categories']
#                 if categories is not None:
#                     create_categories(categories)
#                 else:
#                     print("Error: Categories data is None")
#             else:
#                 print("Error: Response JSON is None or does not contain expected keys")
#         except ValueError:
#             print("Error: Response is not valid JSON")
#     else:
#         print(f"Error: Failed to fetch data from the API. Status code: {response.status_code}")
#
#
# def create_categories(categories, parent=None):
#     for category_data in categories:
#         category_id = category_data.get('CategoryID')
#         name = category_data.get('CategoryName')
#         img_url = None
#         parent_category = Category.objects.create(
#             categoryId=category_id,
#             name=name,
#             # img_url=img_url,
#             parent=parent
#         )
#         sub_categories = category_data.get('SubCategories', [])
#         if sub_categories:
#             create_categories(sub_categories, parent=parent_category)

# from celery import shared_task
# import requests
# from .models import Category
# from site_market.celery import app
#
#
# @app.task
# def test_task():
#     print('Worked')
#     return True
#
#
# @app.task()
# def update_database():
#     print('hello')
#     api_url = 'https://b2b.marvel.kz/Api/GetCatalogCategories?user=01itgroup04&password=m_u_oOV8N1&secretKey=&responseFormat=1'
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         data = response.json()  # Assuming the response is JSON
#         categories = data.get('Body', {}).get('Categories', [])
#         create_categories(categories)
#     else:
#         pass
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
#             img_url=img_url,
#             parent=parent
#         )
#         sub_categories = category_data.get('SubCategories', [])
#         if sub_categories:
#             create_categories(sub_categories, parent=parent_category)
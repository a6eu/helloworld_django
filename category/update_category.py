# from django.core.management.base import BaseCommand
# from category.models import Category
# import requests
#
#
# class Command(BaseCommand):
#     help = 'Update the database from another API'
#     api_url = requests.get(
#         'https://b2b.marvel.kz/Api/GetCatalogCategories?user=01itgroup04&password=m_u_oOV8N1&secretKey=&responseFormat=1')
#
#     def handle(self, *args, **options):
#         response = requests.get(self.api_url)
#         if response.status_code == 200:
#             data = response.json()  # Assuming the response is JSON
#             categories = data.get('Body', {}).get('Categories', [])
#             self.create_categories(categories)
#         else:
#             self.stdout.write(self.style.ERROR('Failed to fetch data from the API'))
#
#     def create_categories(self, categories, parent=None):
#         for category_data in categories:
#             category_id = category_data.get('CategoryID')
#             name = category_data.get('CategoryName')
#             img_url = None  # You need to determine how to handle image URLs
#             parent_category = Category.objects.create(
#                 categoryId=category_id,
#                 name=name,
#                 img_url=img_url,
#                 parent=parent
#             )
#             sub_categories = category_data.get('SubCategories', [])
#             if sub_categories:
#                 self.create_categories(sub_categories, parent=parent_category)
#

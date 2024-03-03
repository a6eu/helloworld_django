import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_market.settings')
app = Celery('site_market')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'get_categories_every_5_minutes': {
    #     'task': 'category.tasks.update_categories',
    #     'schedule': crontab(minute='*/5')
    # },
    'get_products_every_5_minutes': {
        'task': 'products.tasks.update_product_images',
        'schedule': crontab(minute='*/20'),
    },
}
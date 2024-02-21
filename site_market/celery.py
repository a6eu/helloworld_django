# import os
# from celery import Celery
# from celery.schedules import crontab
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site_market.settings')
# app = Celery('site_market')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
#
# app.conf.beat_schedule = {
#     'get_categories_every_1_minutes': {
#         'task': 'category.tasks.test_task',
#         'schedule': crontab(minute='*/1')
#     },
# }
from django.urls import path
from .views import *

urlpatterns = [
    path('demands/', DemandView.as_view(), name='demand_view'),

]
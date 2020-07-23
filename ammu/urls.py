from django.urls import path

from .views import *

urlpatterns = [
    path('post/', create_new_post),
]


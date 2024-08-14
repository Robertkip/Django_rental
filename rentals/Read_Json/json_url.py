from django.urls import path
from .json_views import read_json, single_json


path('read_json', read_json, name='read_json'),
path('single_json/<str:module>', single_json, name='single_json')
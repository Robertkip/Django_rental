from django .urls import path
from .country_views import country_create, country_list, country_detail


urlpatterns = [
    path('country/store', country_create, name='country-create'),
    path('country/list', country_list, name='country-list'),
    path('country/<int:pk>/', country_detail, name='country-detail'),
]
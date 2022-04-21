from django.contrib import admin
from django.urls import path

from promocode.views import generate_promocode, check_promocode

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate/', generate_promocode, name='generate'),
    path('check/', check_promocode, name='check'),
]

from django.contrib import admin
from django.urls import path, include
from toll_system.views import home  # import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('toll_system.urls')),
    path('', home),  # root URL
]

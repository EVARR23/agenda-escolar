
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', admin.site.urls),
    path('home/', views.home)
  
]

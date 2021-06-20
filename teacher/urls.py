from django.urls import path, re_path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'teacher'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:teacher_id>/', views.profile, name='profile'),
    path('create/', views.create, name='create'),
    path('create_bulk/', views.create_bulk, name='create_bulk'),
    path('filter/', views.filter, name='filter')
]

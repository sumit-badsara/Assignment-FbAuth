from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('pages', views.pages, name='pages'),
    path('edit/<int:id>', views.edit, name='edit'), 
    path('update/<int:id>', views.update, name='update')
]

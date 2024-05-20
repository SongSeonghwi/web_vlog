from django.urls import path
from . import views

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('jhw_yoon/', views.jhw_yoon, name='jhw_yoon'),
]

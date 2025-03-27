from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommend_movie, name='recommend'),
    path('test/', views.test_recommend, name='test_recommend'),
    path('search/<str:prompt>/', views.direct_recommend, name='direct_recommend'),
] 
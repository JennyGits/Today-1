from django.urls import path
from . import  views

urlpatterns = [
    path('', views.main, name='main'),
    path('index/', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('result/', views.result, name='result'),
    path('addQuestion/', views.addQuestion, name='addQuestion'),
    path('add/', views.add, name='add'),
]


app_name = 'polls'
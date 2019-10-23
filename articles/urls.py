from django.urls import path, include
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update/', views.update, name='update'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('<int:article_pk>/like/', views.like, name='like'),
    path('<int:article_pk>/create_com/', views.create_com, name='create_com'),
    # /articles/3/create_com/5/delete/
    path('<int:article_pk>/create_com/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:article_pk>/follow/<int:user_pk>/', views.follow, name='follow'),
]



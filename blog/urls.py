from django.urls import path
from . import views

urlpatterns = [
    path('update_post/<int:pk>/',views.PostUpdate.as_view()),
    path('create_post/',views.PostCreate.as_view()),
    path('tag/<str:slug>/',views.tag_page),
    path('category/<str:slug>/',views.category_page),
    path('',views.PostList.as_view()), #blog.urls.py로 위임
    path('<int:pk>/',views.PostDetail.as_view())
]

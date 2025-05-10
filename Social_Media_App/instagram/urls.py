from django.contrib import admin
from django.urls import path
from socialmedia import settings
from instagram import views
from django.conf.urls.static import static

urlpatterns = [

    path('',views.home),
    path('login/',views.login),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout),
    path('upload/', views.upload, name='upload'),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('post/<str:id>/', views.home_post, name='home_post'),
    path('explore',views.explore),
    path('profile/<str:id_user>', views.profile),
    path('delete/<str:id>', views.delete),
    path('search-results/', views.search_results, name='search_results'),
    path('follow', views.follow, name='follow'),
 
    
]
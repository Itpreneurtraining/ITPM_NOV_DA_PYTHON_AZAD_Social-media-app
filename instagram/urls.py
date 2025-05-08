from django.contrib import admin
from django.urls import path
from socialmedia import settings
from instagram import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    path('signup/',views.signup,name='signup'),
]
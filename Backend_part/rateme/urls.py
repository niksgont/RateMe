"""
URL configuration for rateme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main.views import category_detail, all_categories, login_view, signup_view \
    , create_review, get_categories, create_category

urlpatterns = [
    path('create_category/', create_category, name='create_category'),
    path('get_categories/', get_categories, name='get_categories'),
    path('create_review/', create_review, name='create_review'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('categories/', all_categories, name='categorys'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

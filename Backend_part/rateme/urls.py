"""
URL configuration for the rateme project.

The `urlpatterns` list routes URLs to views. The routing is done based on the URL pattern. The pattern is matched against
the URL, and if the pattern matches, the corresponding view function is invoked.

For more information, see: https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

# Django imports
from django.contrib import admin
from django.urls import path, include
from main.views import *
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

# Importing necessary modules for the API documentation
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Importing necessary modules for the API views
from rest_framework.routers import DefaultRouter
from main.views import ReviewViewSet, CategoryViewSet, RateViewSet

# Creating a router object and registering our ViewSets with it.
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'rates', RateViewSet)

# Create a schema view for the API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Reviews API",
      default_version='v1',
      description="API for reviews",
      contact=openapi.Contact(email="contact@yourcompany.local"),
      license=openapi.License(name="Your License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# URL patterns for the views
urlpatterns = [
   path('authors/', authors_view, name='authors'), # Authors page
   path('help/', help_view, name='help'), # Help page
   path('search/', search, name='search'), # Search functionality
   path('user/', user_page, name='user_page'), # User page
   path('review/<int:review_id>/', review_detail, name='review_detail'), # Review detail page
   path('review/<int:review_id>/add_review/', add_review, name='add_review'), # Add review page
   path('create_category/', create_category, name='create_category'), # Create category page
   path('get_categories/', get_categories, name='get_categories'), # Get categories page
   path('create_review/', create_review, name='create_review'), # Create review page
   path('categories/', all_categories, name='categories'), # All categories page
   path('category/<int:category_id>/', category_detail, name='category_detail'), # Category detail page

   # Users paths
   path('admin/', admin.site.urls),
   path('login/', login_view, name='login'),
   path('signup/', signup_view, name='signup'),
   path('signout/', signout_view, name='signout'),
   #  path("accounts/", include("django.contrib.auth.urls"), name='auth'),

   # API documentation paths
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   # API paths
   path('api/', include(router.urls)),

   # Main page
   path('', main_page, name='main_page'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG: # Only in development
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
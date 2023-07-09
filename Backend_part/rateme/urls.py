from django.contrib import admin
from django.urls import path, include
from main.views import *


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from main.views import ReviewViewSet, CategoryViewSet, RateViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'rates', RateViewSet)

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

urlpatterns = [
    path('user/', user_page, name='user_page'),
    path('review/<int:review_id>/', review_detail, name='review_detail'),
    path('review/<int:review_id>/add_review/', add_review, name='add_review'),
    path('create_category/', create_category, name='create_category'),
    path('get_categories/', get_categories, name='get_categories'),
    path('create_review/', create_review, name='create_review'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('signout/', signout_view, name='signout'),
    path('categories/', all_categories, name='categories'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls"), name='auth'),
    path('api/', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', main_page, name='main_page'),
]

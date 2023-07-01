from django.contrib import admin

from .models import Review, Category, Rate

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Rate)

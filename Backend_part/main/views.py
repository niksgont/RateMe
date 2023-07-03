from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import ReviewForm, CategoryForm
from django.http import JsonResponse, HttpResponse
import json
from django.core import serializers

from rest_framework import viewsets
from main.models import Review, Category, Rate
from main.serializers import ReviewSerializer, CategorySerializer, RateSerializer


User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'category_detail.html', {'category': category})


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'all_categories.html', {'categories': categories})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')
    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error': 'Username already exists.'})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, 'signup.html', {'error': 'Email already exists.'})
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    return redirect('login')
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})
    else:
        return render(request, 'signup.html')
    
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.category, _ = Category.objects.get_or_create(name=form.cleaned_data['category'])
            review.save()
            return redirect('categories')
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form})


def get_categories(request):
    categories = serializers.serialize('json', Category.objects.all())
    return JsonResponse(categories, safe=False)

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorys')  # Change 'categories' to 'categorys'
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form})

def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categorys')  # or wherever you want to redirect after successful form submission
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})
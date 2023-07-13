from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import ReviewForm, CategoryForm, RateForm
from django.http import JsonResponse, HttpResponse
import json
from django.core import serializers
from django.core.exceptions import ValidationError

from rest_framework import viewsets
from main.models import Review, Category, Rate
from main.serializers import ReviewSerializer, CategorySerializer, RateSerializer

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


User = get_user_model()

def category_autocomplete(request):
    """
    Returns a list of all categories for autocompletion feature in JSON format.
    """
    categories = Category.objects.values_list('name', flat=True)
    data = list(categories)
    return JsonResponse(data, safe=False)

def main_page(request):
    """
    This function handles both GET and POST requests for the main page of the website.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    If the HTTP method is GET:
    - All categories are fetched from the database.
    - A new, empty ReviewForm is instantiated.
    - The 'main_page.html' template is rendered, with the categories and the form passed in the context.

    If the HTTP method is POST:
    - All categories are fetched from the database.
    - A ReviewForm is instantiated with the POST data.
    - The form's data is validated:
        - If the form is valid:
            - The form's data is saved to a new Review object, but the object is not saved to the database yet (commit=False).
            - A Category object is gotten or created with the name from the cleaned form data, and it is assigned to the review's category.
            - The current user's ID is assigned to the review's creator ID.
            - The form is saved, which saves the Review object to the database.
            - The user is redirected to the main page.
        - If the form is not valid:
            - The 'main_page.html' template is rendered, with the categories and the invalid form passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.

    Exceptions:
    DoesNotExist: An exception is raised if the Category object does not exist and cannot be created.
    ValidationError: An exception is raised if the form is not valid.
    """
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.category, _ = Category.objects.get_or_create(name=form.cleaned_data['category'])
            review.creator_id = request.user.id
            form.save()
            return redirect('main_page')
    else:
        form = ReviewForm()

    return render(request, 'main_page.html', {'categories': categories, 'form': form, 'user': request.user})


class ReviewViewSet(viewsets.ModelViewSet):
    """
    A Django Rest Framework ViewSet for handling Reviews.

    This class extends the ModelViewSet provided by the Django Rest Framework, 
    which includes actions and handlers for list, create, retrieve, update, 
    partial_update, and destroy operations.

    Attributes:
    queryset (QuerySet): The QuerySet used for the view. This is set to include 
    all objects in the Review model.
    
    serializer_class (Serializer): The serializer class used for validating and 
    transforming the data. This is set to the ReviewSerializer.

    This class uses the default handlers provided by ModelViewSet, 
    but you can add additional methods or override the default handlers if needed.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A Django Rest Framework ViewSet for handling Categories.

    This class extends the ModelViewSet provided by the Django Rest Framework, 
    which includes actions and handlers for list, create, retrieve, update, 
    partial_update, and destroy operations.

    Attributes:
    queryset (QuerySet): The QuerySet used for the view. This is set to include 
    all objects in the Category model.
    
    serializer_class (Serializer): The serializer class used for validating and 
    transforming the data. This is set to the CategorySerializer.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RateViewSet(viewsets.ModelViewSet):
    """
    A Django Rest Framework ViewSet for handling Rates.

    This class extends the ModelViewSet provided by the Django Rest Framework, 
    which includes actions and handlers for list, create, retrieve, update, 
    partial_update, and destroy operations.

    Attributes:
    queryset (QuerySet): The QuerySet used for the view. This is set to include 
    all objects in the Rate model.
    
    serializer_class (Serializer): The serializer class used for validating and 
    transforming the data. This is set to the RateSerializer.
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


def category_detail(request, category_id):
    """
    Detail view for a single Category.

    This view fetches a category by its ID (or renders a 404 page if no such 
    category exists) and then renders it to the 'category_detail.html' template.

    Args:
    category_id (int): The ID of the category to retrieve.
    """
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'category_detail.html', {'category': category})


def all_categories(request):
    """
    List view for all Categories.

    This view fetches all categories and then renders them to the 'all_categories.html' template.
    """
    categories = Category.objects.all()
    return render(request, 'all_categories.html', {'categories': categories})

def login_view(request):
    """
    This function handles both GET and POST requests for the login page of the website.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    If the HTTP method is GET:
    - The 'accounts/login.html' template is rendered.

    If the HTTP method is POST:
    - The username and password are extracted from the POST data.
    - The user is authenticated.
        - If the user is authenticated successfully:
            - The user is logged in.
            - The user is redirected to the main page.
        - If the user is not authenticated successfully:
            - The 'accounts/login.html' template is rendered, with an error message passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'accounts/login.html')
    
def signup_view(request):
    """
    This function handles both GET and POST requests for the signup page of the website.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    If the HTTP method is GET:
    - The 'accounts/signup.html' template is rendered.

    If the HTTP method is POST:
    - The username, email, and password are extracted from the POST data.
    - It is checked if the entered password matches the confirmed password, and if the username and email do not already exist.
        - If all checks pass:
            - A new user is created and saved.
            - The user is redirected to the login page.
        - If any check fails:
            - The 'accounts/signup.html' template is rendered, with an error message passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'accounts/signup.html', {'error': 'Username already exists.'})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, 'accounts/signup.html', {'error': 'Email already exists.'})
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    return redirect('login')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match.'})
    else:
        return render(request, 'accounts/signup.html')
    
def signout_view(request):
    """
    This function handles the log out action of the user.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    The user is logged out and then redirected to the main page.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response, which is a redirection to the main page.
    """
    logout(request)
    return redirect('main_page')


def create_review(request):
    """
    This function handles both GET and POST requests for the create review page of the website.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    If the HTTP method is GET:
    - A new, empty ReviewForm is instantiated.
    - The 'create_review.html' template is rendered, with the form passed in the context.

    If the HTTP method is POST:
    - A ReviewForm is instantiated with the POST data.
    - The form's data is validated:
        - If the form is valid:
            - The form's data is saved to a new Review object, but the object is not saved to the database yet (commit=False).
            - The current user's ID is assigned to the review's creator ID.
            - A Category object is gotten or created with the name from the cleaned form data, and it is assigned to the review's category.
            - The review is saved, which saves the Review object to the database.
            - The user is redirected to the categories page.
        - If the form is not valid:
            - The 'create_review.html' template is rendered, with the invalid form passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.creator_id = request.user.id
            form.instance.category, _ = Category.objects.get_or_create(name=form.cleaned_data['category'])
            try:
                form.instance.full_clean()
            except ValidationError:
                return render(request, 'create_review.html', {'form': form})
            form.save()
            return redirect('categories')
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form})

def get_categories(request):
    """
    This function retrieves all the Category objects from the database, serializes them to JSON, and returns them in a JsonResponse.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    Returns:
    JsonResponse: The JsonResponse object representing the HTTP response, containing all categories serialized to JSON.
    """
    categories = serializers.serialize('json', Category.objects.all())
    return JsonResponse(categories, safe=False)

def create_rate(request):
    """
    This function handles both GET and POST requests for the create rate page of the website.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    If the HTTP method is GET:
    - A new, empty RateForm is instantiated.
    - The 'create_rate.html' template is rendered, with the form passed in the context.

    If the HTTP method is POST:
    - A RateForm is instantiated with the POST data.
    - The form's data is validated:
        - If the form is valid:
            - The form's data is saved to a new Rate object, but the object is not saved to the database yet (commit=False).
            - A Review object is gotten or created with the name from the cleaned form data, and it is assigned to the rate's review.
            - The rate is saved, which saves the Rate object to the database.
            - The user is redirected to the categories page.
        - If the form is not valid:
            - The 'create_rate.html' template is rendered, with the invalid form passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.review, _ = Review.objects.get_or_create(name=form.cleaned_data['review'])
            rate.save()
            return redirect('categories')
    else:
        form = RateForm()
    return render(request, 'create_rate.html', {'form': form})


@csrf_exempt
def create_category(request):
    """
    This function handles both GET and POST requests to create a category. 

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    If the HTTP method is POST:
    - The 'name' value is fetched from the POST data.
    - A Category object is gotten or created with the 'name'.
        - If a new category was created:
            - A JsonResponse is returned with a message stating the category was successfully created and a status code of 201.
        - If the category already existed:
            - A JsonResponse is returned with a message stating the category already exists and a status code of 200.

    If the HTTP method is not POST:
    - A JsonResponse is returned with an error message stating the request is invalid and a status code of 400.

    Returns:
    JsonResponse: The JsonResponse object representing the HTTP response, containing a message and a status code.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        category, created = Category.objects.get_or_create(name=name)
        if created:
            return JsonResponse({'message': 'Category created successfully'}, status=201)
        else:
            return JsonResponse({'message': 'Category already exists'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def review_detail(request, review_id):
    """
    This function handles both GET and POST requests for the review detail page of a specific review.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.
    review_id (int): The ID of the review.

    If the HTTP method is GET:
    - The review with the given ID is fetched from the database, raising a 404 error if no such review exists.
    - A new, empty ReviewForm is instantiated.
    - The 'review_detail.html' template is rendered, with the review and the form passed in the context.

    If the HTTP method is POST:
    - The review with the given ID is fetched from the database, raising a 404 error if no such review exists.
    - A ReviewForm is instantiated with the POST data.
    - The form's data is validated:
        - If the form is valid:
            - The form's data is saved to a new Review object, but the object is not saved to the database yet (commit=False).
            - The review's text, category, and creator are assigned to the new review.
            - The new review is saved, which saves the Review object to the database.
            - The user is redirected to the review detail page of the new review.
        - If the form is not valid:
            - The 'review_detail.html' template is rendered, with the review and the invalid form passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    review = get_object_or_404(Review, pk=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.review_text = review.review_text
            new_review.category = review.category
            new_review.creator = request.user
            new_review.save()
            return redirect('review_detail', review_id=review_id)
    else:
        form = ReviewForm()

    return render(request, 'review_detail.html', {'review': review, 'form': form})

@login_required
def user_page(request):
    """
    This function handles GET requests for the user's page, showing all reviews created by the user.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    The function is decorated with the login_required decorator, so it requires the user to be authenticated.

    - All reviews created by the current user are fetched from the database.
    - The 'user_page.html' template is rendered, with the reviews passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """

    reviews = Review.objects.filter(creator=request.user)
    return render(request, 'user_page.html', {'reviews': reviews})

def add_review(request, review_id):
    """
    This function handles both GET and POST requests for the page to add a review to a specific category.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.
    review_id (int): The ID of the review.

    If the HTTP method is GET:
    - The review with the given ID is fetched from the database, raising a 404 error if no such review exists.
    - A new, empty ReviewForm is instantiated.
    - The 'add_review.html' template is rendered, with the review and the form passed in the context.

    If the HTTP method is POST:
    - The review with the given ID is fetched from the database, raising a 404 error if no such review exists.
    - A ReviewForm is instantiated with the POST data.
    - The form's data is validated:
        - If the form is valid:
            - The form's data is saved to a new Review object, but the object is not saved to the database yet (commit=False).
            - The original review's category and name, and the current user, are assigned to the new review.
            - The new review is saved, which saves the Review object to the database.
            - The user is redirected to the review detail page of the new review.
        - If the form is not valid:
            - The 'add_review.html' template is rendered, with the original review and the invalid form passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.category = review.category
            new_review.creator = request.user
            new_review.name = review.name
            new_review.save()
            return redirect('review_detail', review_id=review.id)
    else:
        form = ReviewForm()
    
    return render(request, 'add_review.html', {'review': review, 'form': form})


def search(request):
    """
    This function handles GET requests for the search page.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    - The 'q' value is fetched from the GET data, which represents the search query.
    - All categories and reviews that contain the search query in their name or review text, respectively, are fetched from the database.
    - The 'search_results.html' template is rendered, with the matching categories and reviews passed in the context.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    query = request.GET.get('q')
    categories = Category.objects.filter(name__icontains=query)
    reviews = Review.objects.filter(review_text__icontains=query)
    return render(request, 'search_results.html', {'categories': categories, 'reviews': reviews})


def help_view(request):
    """
    This function handles GET requests for the help page.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    - The 'help.html' template is rendered.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    return render(request, 'help.html')

def authors_view(request):
    """
    This function handles GET requests for the authors page.

    Parameters:
    request (HttpRequest): The Django HttpRequest object representing the HTTP request.

    - The 'authors.html' template is rendered.

    Returns:
    HttpResponse: The HttpResponse object representing the HTTP response.
    """
    return render(request, 'authors.html')
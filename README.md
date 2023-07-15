# Django Review Platform

## Overview

This Django-based application is a user-friendly platform that enables users to write, view, and rate reviews across various categories. It leverages the powerful features of Django and the Django Rest Framework to provide a robust and intuitive interface.

## Core Features

1. **User Authentication**: Built-in Django user authentication system for user registration, login, and logout functionality.

2. **Review Posting**: Users can post reviews under various categories and rate them.

3. **Search Functionality**: Enables users to search for reviews and categories efficiently.

4. **API Endpoints**: Supports CRUD operations via API endpoints that interact with the application's models.

5. **Error Handling**: Includes comprehensive handling of 404 errors and form validation errors.

## Installation

To get this application up and running, follow these steps:

1. Clone this repository to your local machine.

2. Navigate to the root directory of the project.

3. Install the required packages using pip:
   
   ```
   pip install -r requirements.txt
   ```

4. Once the packages are installed, run the following command to start the Django server:

   ```
   python manage.py runserver
   ```

5. Visit `localhost:8000` in your web browser to access the application.

## Usage

After logging in or signing up, users can create reviews under various categories. Each review can be rated, and the cumulative ratings are displayed on the review's page. Users can also use the search bar to find specific reviews or categories.

## API

The application provides a series of API endpoints for performing CRUD operations on reviews, categories, and ratings. Swagger UI is integrated for easy interaction with the API.

## Contributing

We welcome contributions to this project. Please feel free to fork this repository, make your changes, and open a pull request to propose changes.

## Contact

If you have any questions or suggestions, please feel free to reach out.

Enjoy using our Django Review Platform!

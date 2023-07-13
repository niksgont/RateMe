from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

def validate_range(value):
    """
    This function validates if a provided integer is in the range from 0 to 5, inclusive.

    Parameters:
    value (int): The value to be validated.

    Raises:
    ValidationError: If the value is not in the range 0-5.
    """
    if value < 0 or value > 5:
        raise ValidationError("Number must be in range 0-5")

class Category(models.Model):
    """
    This model represents a Category for reviews.

    Attributes:
    name (CharField): The name of the category. This field is required and can take up to 200 characters.

    Methods:
    __str__: Returns a string representation of the Category object, which is its name.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    This model represents a Review of a category.

    Attributes:
    review_text (CharField): The text of the review. This field is required and can take up to 200 characters.
    description (TextField): The detailed description of the review.
    rate (IntegerField): The rating given in the review. This field is required and is validated by the 'validate_range' function.
    pub_date (DateTimeField): The date and time when the review was published. This field is automatically set when the review is created.
    category (ForeignKey): A reference to the category that the review belongs to. If the category is deleted, the review is also deleted.
    creator (ForeignKey): A reference to the User who created the review. If the user is deleted, the 'creator' field is set to NULL.
    image (ImageField): An image that is associated with the review. This field is optional.

    Methods:
    __str__: Returns a string representation of the Review object, which is its review_text.
    """
    review_text = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.IntegerField(default=0, validators=[validate_range])
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='reviews')
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)

    def __str__(self):
        return self.review_text

class Rate(models.Model):
    """
    This model represents a Rate given to a review.

    Attributes:
    review (ForeignKey): A reference to the Review that the rate belongs to. If the review is deleted, the rate is also deleted.
    rate_field (IntegerField): The rating value. This field is required and is validated by the 'validate_range' function.

    Methods:
    __str__: Returns a string representation of the Rate object, which is its rate_field.
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='rates')
    rate_field = models.IntegerField(validators=[validate_range])

    def __str__(self):
        return str(self.rate_field)


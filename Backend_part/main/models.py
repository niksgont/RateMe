from django.core.exceptions import ValidationError
from django.db import models

def validate_range(value):
    if value < 0 or value > 5:
        raise ValidationError("Number must be in range 0-5")

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Review(models.Model):
    review_text = models.CharField(max_length=200)
    description = models.TextField()
    rate = models.IntegerField(default=0, validators=[validate_range])
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.review_text

class Rate(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='rates')
    rate_field = models.IntegerField(validators=[validate_range])

    def __str__(self):
        return str(self.rate_field)


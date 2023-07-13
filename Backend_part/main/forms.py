from django import forms
from .models import Review, Category

class CategoryForm(forms.ModelForm):
    """
    This form is used for creating and updating Category instances.

    It is a ModelForm, which means it is directly tied to the Category model. The fields of the form correspond to the fields of the model.

    Attributes:
    Meta: This inner class defines metadata for the form, such as the model the form is tied to and the fields that should be included on the form.

    The fields included in this form are:
    - name
    """
    class Meta:
        model = Category
        fields = ['name']

class ReviewForm(forms.ModelForm):
    """
    This form is used for creating and updating Review instances.

    It is a ModelForm, which means it is directly tied to the Review model. The fields of the form correspond to the fields of the model.

    Attributes:
    Meta: This inner class defines metadata for the form, such as the model the form is tied to and the fields that should be included on the form, and the widgets to be used for rendering each field.

    The fields included in this form are:
    - review_text
    - category
    - description
    - rate

    Each field is rendered using a specific widget, defined in the 'widgets' dictionary. These widgets have been customized with CSS classes for styling.
    """
    class Meta:
        model = Review
        fields = ['review_text', 'category', 'description', 'rate', 'image']
        widgets = {
            'review_text': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class RateForm(forms.Form):
    """
    This form is used for creating Rate instances. 

    It is not a ModelForm, but a regular Form. This means it's not tied to any specific model, but instead defines its fields manually.

    The fields included in this form are:
    - review: A dropdown field which lets the user select from all existing Review instances.
    - rate_field: An integer field which lets the user input a rating.

    Each field is rendered using a specific widget, defined in the field declaration. These widgets have been customized with CSS classes for styling.
    """
    review = forms.ModelChoiceField(queryset=Review.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    rate_field = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

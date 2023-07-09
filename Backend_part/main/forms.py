from django import forms
from .models import Review, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'category', 'description', 'rate']
        widgets = {
            'review_text': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RateForm(forms.Form):
    review = forms.ModelChoiceField(queryset=Review.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    rate_field = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

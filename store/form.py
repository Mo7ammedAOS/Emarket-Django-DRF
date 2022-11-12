from store.models import ReviewRate
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRate
        fields = ['subject', 'review', 'rating']
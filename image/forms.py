from .models import Images
from django import forms

class ImageForm(forms.ModelForm):
        class Meta:
            model=Images
            fields = ['title','content','imagesrc']
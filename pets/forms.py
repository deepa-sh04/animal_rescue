# D:\project1\animal_rescue\pets\forms.py

from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'age', 'image','location']        
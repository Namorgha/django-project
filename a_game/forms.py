from django.forms import ModelForm
from django import forms
from .models import *

class NewGameForm(ModelForm):
    class Meta:
        model = GameModel
        fields = ['room_name']
        widgets = {
            "room_name": forms.TextInput(attrs={
                'placeholder': 'Add name ...',
                'class': 'p-4 text-black',
                'maxlength': '300',  
                'autofocus': True,
            }),
        }


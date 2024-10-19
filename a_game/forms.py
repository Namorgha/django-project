from django.forms import ModelForm
from django import forms
from .models import *


class GameGoalsForm(ModelForm):
    class Meta:
        model = Goal
        fields = ['player', 'game']
        widgets = {
            'player': forms.Select(attrs={'class': 'form-control'}),
            'game': forms.Select(attrs={'class': 'form-control'}),
        }

class NewGameForm(ModelForm):
    class Meta:
        model = GameRoom
        fields = ['gamegroup_name']
        widgets = {
            "gamegroup_name": forms.TextInput(attrs={
                'placeholder': 'Add name ...',
                'class': 'p-4 text-black',
                'maxlength': '30',  # Match the model's max_length
                'autofocus': True,
            }),
        }

    def clean_gamegroup_name(self):
        name = self.cleaned_data.get('gamegroup_name')
        if GameGroup.objects.filter(gamegroup_name=name).exists():
            raise forms.ValidationError("A game group with this name already exists.")
        return name


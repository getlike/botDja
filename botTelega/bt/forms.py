from django import forms

from .models import Profile

class ProfileForn(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id', #скрываем айди
            'name',
        )
        widgets = {
            'name' : forms.TextInput,
        }
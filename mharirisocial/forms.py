from django import forms
from django.forms.extras.widgets import SelectDateWidget

import account.forms
from mharirisocial.profiles.models import Profile

class SignupForm(account.forms.SignupForm):
    
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))
    

class SearchForm(forms.Form):
    journalist = forms.ModelChoiceField(Profile.objects.all)

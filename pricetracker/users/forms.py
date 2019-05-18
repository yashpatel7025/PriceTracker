from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User#this tells us model which affected by form.save() would be User model
        fields = ['username', 'email', 'password1', 'password2']#this tells us what field you want in your modified form and 
                                                                    #and in what order
class UserUpdateForm(forms.ModelForm):
		email = forms.EmailField()
		class Meta:
			model = User
			fields = ['username', 'email']
class ProfileUpdateForm(forms.ModelForm):
		class Meta:
			model = Profile
			fields = ['image']
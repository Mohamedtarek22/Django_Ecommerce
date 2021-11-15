
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.forms import UserChangeForm
from user.models import UserProfile
from django.forms import TextInput, EmailInput, Select, FileInput, fields

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label= 'User Name :')
    email = forms.EmailField(max_length=200,label= 'Email :')
    first_name = forms.CharField(max_length=100,label= 'First Name :')
    last_name = forms.CharField(max_length=100,label= 'Last Name :')
    # mobile=forms.CharField(max_length=100,label='Mobile')
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password1', 'password2', )

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name' }),
        }

CITY = [
    ('cairo', 'cairo'),
    ('giza', 'giza'),
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country',
                  # 'image','language'
                  )
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input','placeholder':'phone'}),
            'address'   : TextInput(attrs={'class': 'input','placeholder':'address'}),
            'city'      : Select(attrs={'class': 'input','placeholder':'city'},choices=CITY),
            'country'   : TextInput(attrs={'class': 'input','placeholder':'country' }),
            # 'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }

class AddressBookForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('address','phone','status_address')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input','placeholder':'Mobile Number'}),
            # 'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }



class ProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields=('username', 'email','first_name','last_name' )

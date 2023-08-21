from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from theblog.models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs = {'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs = {'class': 'form-control'}))
    is_active = forms.CharField(max_length=150, widget=forms.CheckboxInput(attrs = {'class': 'form-check'}))
    

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'github_url')
        widgets = {
            'bio': forms.Textarea(attrs = {'class': 'form-control'}),
            #'profile_pic': forms.TextInput(attrs = {'class': 'form-control'}),
            'website_url': forms.TextInput(attrs = {'class': 'form-control'}),
            'facebook_url': forms.TextInput(attrs = {'class': 'form-control'}),
            'twitter_url': forms.TextInput(attrs = {'class': 'form-control'}),
            'instagram_url': forms.TextInput(attrs = {'class': 'form-control'}),
            'github_url': forms.TextInput(attrs = {'class': 'form-control'}),
        }
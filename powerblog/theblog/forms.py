from django import forms
from .models import Post, Category

#choices = [('Abstract', 'Abstract'), ('Tech', 'Tech'), ('Interests', 'Interests')]

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'header_image', 'author', 'category', 'body', 'snippet')

        widgets = {
            'title' : forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a Title'}),
            'title_tag' : forms.TextInput(attrs = {'class': 'form-control'}),
            'author' : forms.TextInput(attrs = {'class': 'form-control', 'value': "", 'id': 'user', 'type': 'hidden'}),
            'header_image' : forms.FileInput(attrs={'class':'form-control'}),
            #'author' : forms.Select(attrs = {'class': 'form-control'}),
            'category' : forms.Select(choices= choice_list, attrs = {'class': 'form-control'}),
            'body' : forms.Textarea(attrs = {'class': 'form-control'}),
            'snippet' : forms.Textarea(attrs = {'class': 'form-control'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'body', 'snippet')

        widgets = {
            'title' : forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Add a Title'}),
            'title_tag' : forms.TextInput(attrs = {'class': 'form-control'}),
            'body' : forms.Textarea(attrs = {'class': 'form-control'}),
            'snippet' : forms.Textarea(attrs = {'class': 'form-control'}),
        }
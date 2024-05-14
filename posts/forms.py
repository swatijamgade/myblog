from django import forms
from .models import Comment


# Normal Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def __str__(self):
        return self.username


# Model Form
class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
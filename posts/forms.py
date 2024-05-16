from django import forms
from .models import Comment


# Model Form
class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
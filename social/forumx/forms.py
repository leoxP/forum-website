from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(required=True,
            widget=forms.widgets.Textarea(
                attrs={
                    "placeholder": "Enter your post",
                    "class": "form-control"
                }
                ),
            label="",
            )
    
    class Meta:
        model = Post
        fields = ['content']  
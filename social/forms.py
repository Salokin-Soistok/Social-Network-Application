from django import forms  # Import the forms module from Django
from .models import Post, Comment  # Import the Post and Comment models

class PostForm(forms.ModelForm):  # Create a form for the Post model
    body = forms.CharField(label='', widget=forms.Textarea(attrs={  # Customize the body field
        'rows': '3',  # Set the number of visible text lines
        'placeholder': 'Say Something...'  # Placeholder text
    }))

    class Meta:  # Meta class to configure the form
        model = Post  # Specify the model to use
        fields = ['body']  # Fields to include in the form

class CommentForm(forms.ModelForm):  # Create a form for the Comment model
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={  # Customize the comment field
        'rows': '3',  # Set the number of visible text lines
        'placeholder': 'Say Something...'  # Placeholder text
    }))

    class Meta:  # Meta class to configure the form
        model = Comment  # Specify the model to use
        fields = ['comment']  # Fields to include in the form

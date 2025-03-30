from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    """
    Form for sharing blog posts via email.
    
    This form collects information needed to share a blog post with someone:
    - Sender's name
    - Sender's email
    - Recipient's email
    - Optional comments from the sender
    """
    name = forms.CharField(max_length=25)  # Sender's name
    email = forms.EmailField()  # Sender's email address
    to = forms.EmailField()  # Recipient's email address
    comments = forms.CharField(required=False, widget=forms.Textarea)  # Optional message

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 10, "cols": 40})}

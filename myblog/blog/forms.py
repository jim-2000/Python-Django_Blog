from django import forms
from .models import Comment
# .>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class EmailForms(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment')
    
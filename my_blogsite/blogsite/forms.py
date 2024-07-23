from django import forms

from . import models


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
    def clean_to(self):
        to_emails = self.cleaned_data.get('to_email')
        if not to_emails:
            raise forms.ValidationError('You must enter at least one recipient email.')
        if len(to_emails.split()) > 5:
            raise forms.ValidationError('You can only enter up to five recipient emails.')
        return to_emails
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['name', 'email', 'body']
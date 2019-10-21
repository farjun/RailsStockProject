#__author__ = Mohammad Abdin
from django import forms
from .models import Profile
from django.contrib.auth.models import User



""" this is the form for updating the user's profile."""
class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    job = forms.CharField(required=True)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'job' )

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(UpdateProfile, self).save(commit=False)
        user.email = self.cleaned_data['email']
        print("save profile .....")
        if commit:
            user.save()

        return user

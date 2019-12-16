#__author__ = Mohammad Abdin
from django import forms
from .models import Profile
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name' )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('job', 'image')  # Note that we didn't mention user field here.


class UpdateProfile(forms.ModelForm):
    """ this is the form for updating the user's profile"""
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    job = forms.CharField(required=False)
    # my_stocks = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'job' )

    def clean_email(self):
        """ this function checks if the entered email address is already in use"""
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        """ this function saves the edits applied to the to user's profile"""
        user = super(UpdateProfile, self).save(commit=False)
        user.email = self.cleaned_data['email']
        print("save profile .....")
        if commit:
            user.save()
        return user
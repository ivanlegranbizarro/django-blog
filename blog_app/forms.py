from django.contrib.auth.models import User
from .models import Profile, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# SignUpForm
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'image',)


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'content',)

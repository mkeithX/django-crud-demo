from typing import Any, Optional
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from apps.users.models import User, UserProfile
from django import forms
from django_countries.widgets import CountrySelectWidget
from apps.users.widgets import DatePickerInput,  DateTimePickerInput
from django_countries.fields import CountryField
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, password_validation
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.layout import Layout, Field, Submit, Div
from crispy_forms.helper import FormHelper

from django.forms import widgets

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(min_length=4, widget=widgets.TextInput(attrs={'placeholder':"username", "class":"form-control"}))
    email = forms.EmailField(required=True, max_length=30, min_length=3, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}))
    date_of_birth = forms.DateField(required=True, widget=DatePickerInput())
    password2 = forms.CharField(help_text="Confirm password and let's go!",widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}),)


    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        dob = self.cleaned_data["date_of_birth"]
        age = abs(date.today() - dob)
        if (age.days / 365.0) < 18:
            raise forms.ValidationError(
                "You must be at least 18 to signup.",
                code="too_young",
            )
        return cleaned_data
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email already taken.")
        return email
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'date_of_birth', 'password1', 'password2']



class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["username"].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username or email'
        self.fields["password"].label = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("username"),
            Field("password"),
            Field("remember_me"),
        )

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(min_length=4, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(min_length=3, widget=forms.TextInput(attrs={"class":"form-control"}))
    date_of_birth = forms.DateField(required=True, widget=DatePickerInput())


    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "gender", "date_of_birth"]
    

    def clean(self):
        cleaned_data = super(UpdateUserForm, self).clean()
        dob = self.cleaned_data["date_of_birth"]
        age = abs(date.today() - dob)
        if (age.days / 365.0) < 18:
            raise forms.ValidationError(
                "You must be at least 18 years old.",
                code="too_young",
            )
        
        return cleaned_data

class UpdateProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("bio"),
            Field("country"),
            Field("avatar"),
            # Submit("update", "Update", css_class="btn-success")
        )

    class Meta:
        model = UserProfile
        fields = ["bio", "country", "avatar"]
        widgets = {
            "country": CountrySelectWidget(),
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Current password"}),)
    new_password1 = forms.CharField(help_text = 'Passwords:<ul class="form-text text-muted small"><li>CAN\'T be too similar to your other personal information.</li><li>MUST contain at least 9 characters.</li><li>CAN\'T be a commonly used password.</li><li>CAN\'T be entirely numeric.</li></ul>',widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New password"}),)
    new_password2 = forms.CharField(help_text="Confirm password and let's go!", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}),)


    class Meta:
        model = get_user_model()
        fields = ["old_password", "new_password1", "new_password2",]

        
    # def __init__(self, user: AbstractBaseUser | None, *args: Any, **kwargs: Any) -> None:
    #     super(ChangePasswordForm, self).__init__(user, *args, **kwargs)
    
    #     self.fields['new_password1'].widget.attrs['class'] = 'form-control'
    #     self.fields['new_password1'].widget.attrs['placeholder'] = 'New password'
    #     self.fields['new_password1'].label = ''
    #     self.fields['new_password1'].help_text = 'Your Password:<ul class="form-text text-muted small"><li>CAN\'T be too similar to your other personal information.</li><li>MUST contain at least 8 characters.</li><li>CAN\'T be a commonly used password.</li><li>CAN\'T be entirely numeric.</li></ul>'
    #     self.fields['new_password2'].widget.attrs['class'] = 'form-control'
    #     self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm new password'
    #     self.fields['new_password2'].label = ''
    #     self.fields['new_password2'].help_text = '<span class="form-text text-muted"><p>Confirm your new password & let\'s go!</p></span>'

        

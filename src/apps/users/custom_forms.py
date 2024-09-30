# For admin site configuration

from django import forms
from apps.users.models import User
from apps.users.widgets import DatePickerInput
from datetime import date
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)


class CustomSignupForm(UserCreationForm):
    date_of_birth = forms.DateField(required=True, widget=DatePickerInput())

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super(CustomSignupForm, self).clean()
        dob = self.cleaned_data["date_of_birth"]
        age = abs(date.today() - dob)
        if (age.days / 365.0) < 18:
            raise forms.ValidationError(
                "You must be at least 18 to signup.",
                code="too_young",
            )

        return cleaned_data
    


class CustomUpdateForm(UserChangeForm):
    date_of_birth = forms.DateField(required=True, widget=DatePickerInput())

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super(CustomUpdateForm, self).clean()
        dob = self.cleaned_data["date_of_birth"]
        age = abs(date.today() - dob)
        if (age.days / 365.0) < 18:
            raise forms.ValidationError(
                "All users must be at least 18.",
                code="too_young",
            )

        return cleaned_data
            
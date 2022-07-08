from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(driving_license):
    if not driving_license[:3].isalpha() or not driving_license[:3].isupper():
        raise ValidationError("First 3 characters should be uppercase letters")
    if not driving_license[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")
    return driving_license


def validate_registration_number(registration_number):
    if not registration_number[:2].isalpha() or not registration_number[:2].isupper():
        raise ValidationError("First 2 characters should be uppercase letters")
    if not registration_number[2:].isdigit():
        raise ValidationError("Last 5 characters should be digits")
    return registration_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverCreationForm(UserCreationForm):
    license_number = forms.CharField(
        required=True,
        max_length=8,
        label="License number:",
        widget=forms.TextInput(attrs={"placeholder": "FF99999"})
    )

    class Meta:
        model = Driver
        fields = UserCreationForm.Meta.fields + \
            ("first_name", "last_name", "license_number")

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data["license_number"])


class DriverSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username..."})
    )


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    registration = forms.CharField(
        required=True,
        max_length=7,
        label="Registration number:",
        widget=forms.TextInput(attrs={"placeholder": "FF99999"})
    )

    class Meta:
        model = Car
        fields = "__all__"

    def clean_registration(self):
        return validate_registration_number(self.cleaned_data["registration"])

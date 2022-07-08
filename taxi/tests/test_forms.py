from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "FFF99999"
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)



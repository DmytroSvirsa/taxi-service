from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_create_login_required(self):
        response = self.client.get(CAR_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test_password1",
        )
        self.client.force_login(self.user)

    def test_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Car.objects.create(model="test_model", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

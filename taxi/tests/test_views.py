from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

DRIVER_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")
CAR_URL = reverse("taxi:car-list")
CAR_CREATE_URL = reverse("taxi:car-create")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_create_login_required(self):
        response = self.client.get(DRIVER_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_create_login_required(self):
        response = self.client.get(CAR_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_create_login_required(self):
        response = self.client.get(MANUFACTURER_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_username3",
            "test_1qazcde3",
        )
        self.client.force_login(self.user)

    def test_driver_exists(self):
        Driver.objects.create(
            username="test_username2",
            license_number="FFF99999",
        )
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_update_license_number(self):
        driver = Driver.objects.create(
            username="test_username",
            license_number="FFF99999"
        )
        new_data = {
            "license_number": "DDD12345"
        }

        self.client.post(
            reverse("taxi:driver-update", args=[driver.id]), new_data
        )
        updated_driver = Driver.objects.get(id=driver.id)

        self.assertEqual(
            updated_driver.license_number,
            new_data["license_number"],
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test_1qazcde3",
        )
        self.client.force_login(self.user)

    def test_manufacturer(self):
        Manufacturer.objects.create(name="test_name", country="test_country")
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test_1qazcde3",
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

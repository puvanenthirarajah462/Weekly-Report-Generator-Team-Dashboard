from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class DatabaseConfigTests(SimpleTestCase):
    def test_mysql_backend_is_used_when_configured(self):
        self.assertEqual(settings.DATABASES["default"]["ENGINE"], "django.db.backends.mysql")

    def test_mariadb_10_4_compatibility_patch_is_applied(self):
        self.assertTrue(getattr(MySQLDatabaseWrapper, "_weekly_report_dashboard_patched", False))


class RegisterViewTests(APITestCase):
    def test_register_creates_user_with_valid_payload(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "tester",
                "email": "tester@example.com",
                "password": "Test1234!",
                "first_name": "Test",
                "last_name": "User",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(get_user_model().objects.filter(username="tester").exists())

    def test_register_accepts_csrf_checked_requests(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post(
            reverse("register"),
            {
                "username": "tester2",
                "email": "tester2@example.com",
                "password": "Test1234!",
                "first_name": "Test",
                "last_name": "User",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

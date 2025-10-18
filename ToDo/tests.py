from django.test import TestCase
from django.urls import reverse
from .models import Task
from django.contrib.auth.models import User

# Create your tests here.
class AuthTest(TestCase):
    def test_signup_valid(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "email": "nuewuser@gmail.com",
            "first_name": "new",
            "last_name": "user",
            "password1": "StrongPass12345",
            "password2": "StrongPass12345"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("tasks"))

    def setUp(self):
        # create a user for login
        self.user = User.objects.create_user(username="testuser", password="passworASD2ADawdd123")

    def test_login_valid(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "passworASD2ADawdd123"
        } )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("tasks"))

class IndexViewTest(TestCase):
    def setUp(self):
        # create a user for login
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_index_redirects_when_logged_in(self):
        # Log the user in
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("tasks"))

    def test_index_renders_for_anonymous_user(self):
        # No login
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ToDo/index.html")

    def test_logout(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("tasks"))
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("index"))
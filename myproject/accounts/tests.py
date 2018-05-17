from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve,reverse
from .views import signup
from .forms import SignUpForm


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code,200)
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func,signup)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_contains_form(self):
        form  = self.response.context.get('form')
        self.assertIsInstance(form,SignUpForm)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data={
            'username':'john',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url,data)
        self.home_url = reverse('home')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to homepage
        '''
        self.assertRedirects(self.response,self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to arbitary page,the resulting response 
        should have user to its context after successful signup .
        '''
        self.response = self.client.get(self.home_url)
        user = self.response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {}
        self.response = self.client.post(url,data)

    def test_signup_status_code(self):
        '''
        A invalid form submission should return same page
        '''
        self.assertEquals(self.response.status_code,200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
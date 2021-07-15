import pytest
from django.test import TestCase, Client
from .factories import UserFactory
from django.http import HttpResponseRedirect, HttpResponse


class TestCoreViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view_is_resolved(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_about_view_is_resolved(self):
        response = self.client.get('/about', {}, True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')

    def test_community_view_is_resolved(self):
        response = self.client.get('/community', {}, True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/community.html')

    def test_support_versioning_view_is_resolved(self):
        response = self.client.get('/support/versioning', {}, True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'support/versioning.html')

    def test_fallback_views(self):
        response = self.client.get('/doesnt_exist/')
        self.assertEquals(response.status_code, 404)
        self.assertTemplateUsed('404.html')

    def test_fallback_views_unexpected_character(self):
        response1 = self.client.get('/example../')
        self.assertEquals(response1.status_code, 404)
        self.assertTemplateUsed('404.html')
        response2 = self.client.get('/!example/')
        self.assertEquals(response1.status_code, 404)
        self.assertTemplateUsed('404.html')


class SetUpAdminViews(TestCase):
    def setUp(self):
        self.admin_client = Client()
        self.user_client = Client()
        self.admin_user = UserFactory.build(username='admin', is_superuser=True)
        self.admin_user.set_password('admin')
        self.admin_user.save()
        self.user = UserFactory.create(username='user1', is_superuser=False)
        self.user.set_password('user1')
        self.user.save()


class TestAdminResetPasswordView(SetUpAdminViews):
    def setUp(self):
        return super(TestAdminResetPasswordView, self).setUp()

    def test_login_required(self):
        url = '/admin/auth/user/%s/change/resetpassword/' % self.admin_user.id
        response = self.user_client.get(url)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/account/login/?next=' + url)

    def test_user_redirected(self):
        url = '/admin/auth/user/%s/change/resetpassword/' % self.user.id
        login = self.user_client.login(username='user1', password='user1')
        self.assertTrue(login)
        response = self.user_client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEquals(response.url, '/account/login/?next=' + url)

    def test_superuser_required(self):
        url = '/admin/auth/user/%s/change/resetpassword/' % self.admin_user.id
        login = self.admin_client.login(username='admin', password='admin')
        self.assertTrue(login)
        response = self.admin_client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertTemplateUsed(response, 'core/admin_reset_password.html')

    def test_404_url_user_id(self):
        fake_user_id = self.admin_user.id + 100
        url = '/admin/auth/user/%s/change/resetpassword/' % fake_user_id
        login = self.admin_client.login(username='admin', password='admin')
        self.assertTrue(login)
        response = self.admin_client.get(url)
        self.assertEquals(response.status_code, 404)
        self.assertIsInstance(response, HttpResponse)
        self.assertTemplateUsed(response, '404.html')

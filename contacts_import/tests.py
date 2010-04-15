from django.core.urlresolvers import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from contacts_import.models import TransientContact


class BasicTest(TestCase):
    fixtures = ["sample_data.json"]
    
    def setUp(self):
        self.client.login(username="bob", password="abc123")
        self.bob = User.objects.get(username="bob")
    
    def tearDown(self):
        self.client.logout()
    
    def tests_views(self):
        response = self.client.get(reverse("import_contacts"))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse("import_contacts"), {
            "action": "upload_vcard",
        })
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse("authsub_login"))
        self.assertEqual(response.status_code, 302)
    
    def test_contact_display(self):
        TransientContact.objects.create(user=self.bob, name="Bjarne Stroustrup",
            email="bjarne@making.life.hard.com")
        TransientContact.objects.create(user=self.bob, name="Guido van Rossum",
            email="guido@python.org")
        
        response = self.client.get(reverse("import_contacts"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bjarne Stroustrup")
        self.assertContains(response, "Guido van Rossum")

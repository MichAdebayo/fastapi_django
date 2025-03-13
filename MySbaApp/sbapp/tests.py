from django.test import TestCase
from .models import LoanRequestUserProfile

# Create your tests here.
class LoanRequestUserProfileTestCase(TestCase):
    def test_name_uppercase(self):
        """Test that Name is stored in uppercase"""
        instance = LoanRequestUserProfile.objects.create(City="Ayoboenterprise")
        instance.save()

        # Force fetch from the database
        instance.refresh_from_db()

        self.assertEqual(instance.Name, "AYOBOENTERPRISE")


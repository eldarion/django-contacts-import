from datetime import date

from django.db import models

from django.contrib.auth.models import User


class TransientContact(models.Model):
    # The user who created this contact
    owner = models.ForeignKey(User, related_name="imported_contacts")
    
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    
    def __unicode__(self):
        return "%s (%s's contact)" % (self.email, self.owner)

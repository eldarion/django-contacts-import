from datetime import date

from django.db import models

from django.contrib.auth.models import User


class Contact(models.Model):
    # The user who created this contact
    user = models.ForeignKey(User, related_name="contacts")
    
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    added = models.DateField(default=date.today)
    
    # the user(s) this contact ultimately corrosponds to
    users = models.ManyToManyField(User)
    
    def __unicode__(self):
        return "%s (%s's contact)" % (self.email,  self.user)

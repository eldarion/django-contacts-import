from django.contrib import admin

from contacts_import.models import Contact


class ContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(Contact, ContactAdmin)
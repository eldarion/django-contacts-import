from django.contrib import admin

from contacts_import.models import TransientContact


class TransientContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(TransientContact, TransientContactAdmin)
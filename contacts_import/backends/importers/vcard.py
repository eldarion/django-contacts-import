from __future__ import absolute_import

from django import forms

import vobject

from contacts_import.backends.importers.base import Importer


class vCardImportForm(forms.Form):
    
    file = forms.FileField()


class vCardImporter(Importer):
    
    name = "vCard"
    form_class = vCardImportForm
    
    def handle(self, form):
        for entry in vobject.readComponents(form.cleaned_data["file"]):
            yield {
                "email": entry.email.value,
                "name": entry.fn.value
            }

from django import forms

from contacts_import.backends.importers import VcardImporter
from contacts_import.backends.runners import SynchronousRunner


class VcardImportForm(forms.Form):
    vcard_file = forms.FileField(label="vCard File")
    
    def save(self, user, runner_class=SynchronousRunner):
        importer = runner_class(VcardImporter,
            user = user,
            stream = self.cleaned_data["vcard_file"]
        )
        return importer.import_contacts()

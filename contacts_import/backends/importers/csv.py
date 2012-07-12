from __future__ import absolute_import

import csv

from django import forms

from contacts_import.backends.importers.base import Importer


def guess_email(entry):
    if "E-mail Address" in entry: # outlook
        return entry["E-mail Address"]
    if "E-mail 1 - Value" in entry: # gmail
        return entry["E-mail 1 - Value"]
    return None


def guess_name(entry):
    if "Name" in entry: # gmail
        return entry["Name"]
    if "First Name" in entry and "Last Name" in entry: # outlook
        return entry["First Name"] + " " + entry["Last Name"]
    if "Given Name" in entry and "Family Name" in entry: # gmail alt
        return entry["Given Name"] + " " + entry["Family Name"]
    return None


class CSVImportForm(forms.Form):
    
    file = forms.FileField()


class CSVImporter(Importer):
    
    name = "CSV"
    form_class = CSVImportForm
    
    def handle(self, form):
        for entry in csv.DictReader(form.cleaned_data["file"]):
            email = guess_email(entry)
            name = guess_name(entry)
            if email and name:
                yield {"email": email, "name": name}
